import os
import random

import cv2
import numpy as np
import skimage.draw

from deepsport_utilities.calib import set_z_vanishing_point, Point3D, Point2D
from deepsport_utilities.court import Court, BALL_DIAMETER
from deepsport_utilities.transforms import Transform, RandomCropperTransform
from deepsport_utilities.utils import gamma_correction, setdefaultattr
from deepsport_utilities.ds.instants_dataset import View, ViewKey

class AddBallAnnotation(Transform):
    def __call__(self, key, view):
        view.ball = [a for a in view.annotations if a.type == 'ball'][0]
        return view

class UndistortTransform(Transform):
    def __call__(self, key, view):
        all_images = []
        for image in view.all_images:
            all_images.append(cv2.undistort(image, view.calib.K, view.calib.kc))
        view.calib = view.calib.update(kc=np.array([0,0,0,0,0]))
        return view

class RectifyTransform(Transform):
    def __init__(self, output_shape=None):
        self.output_shape = output_shape

    def __call__(self, key, view: View):
        output_shape = (view.image.shape[1], view.image.shape[0]) if self.output_shape is None else self.output_shape
        H = set_z_vanishing_point(view.calib.P, view.calib.img_width, view.calib.img_height)
        all_images = []
        for image in view.all_images:
            all_images.append(cv2.warpPerspective(image, H, output_shape))
        calib = view.calib.update(K=H@view.calib.K)
        return View(all_images, view.box, calib, view.annotations)

class RectifyUndistortTransform(Transform):
    def __init__(self, output_shape=None, interpolation=cv2.INTER_CUBIC):
        self._lookuptables = dict()
        self.output_shape = output_shape
        self.interpolation = interpolation

    def _get_lookuptables(self, arena_label, cam_idx, calib, input_shape):
        cam_key = (arena_label, cam_idx)
        if cam_key not in self._lookuptables:
            # Rescale transform
            output_shape = self.output_shape if self.output_shape else input_shape
            sx = output_shape[0]/input_shape[0]
            sy = output_shape[1]/input_shape[1]
            S = np.array([[sx,0 ,0],
                          [0 ,sy,0],
                          [0 ,0 ,1]])

            # Undistort transform
            map1, map2 = cv2.initUndistortRectifyMap(calib.K, calib.kc, None, S@calib.K, output_shape, cv2.CV_32FC1)
            calib = calib.update(kc=np.array([0,0,0,0,0]), K=S@calib.K, width=output_shape[0], height=output_shape[1])

            # Rectify transform
            H = set_z_vanishing_point(calib.P, output_shape[0], output_shape[1])
            calib = calib.update(K=H@calib.K, kc=np.array([0,0,0,0,0]))
            input_map = np.stack((map1,map2,np.ones_like(map1)), axis=2)
            output_map = np.tensordot(np.linalg.inv(S)@np.linalg.inv(H)@S, input_map, axes=((1),(2))).astype(np.float32)
            map1, map2 = cv2.convertMaps(output_map[0]/output_map[2], output_map[1]/output_map[2], cv2.CV_16SC2) # convertMaps to speed up the lookup

            # Store lookup table
            self._lookuptables[cam_key] = (calib, map1, map2)
        return self._lookuptables[cam_key]

    def __call__(self, view_key: ViewKey, view: View):
        calib, map1, map2 = self._get_lookuptables(view_key.instant_key.arena_label, view_key.camera, view.calib, (view.image.shape[1], view.image.shape[0]))
        all_images = []
        for image in view.all_images:
            all_images.append(cv2.remap(image, map1, map2, self.interpolation))
        return View(all_images, view.box, calib, view.annotations)

class ComputeDiff(Transform):
    def __init__(self, squash=False, inplace=False):
        self.squash = squash
        self.inplace = inplace

    def __call__(self, view_key: ViewKey, view: View):
        diff = np.abs(view.image.astype(np.int32) - view.all_images[1].astype(np.int32)).astype(np.uint8)
        if self.squash:
            diff = np.mean(diff, axis=2).astype(np.uint8)
        if self.inplace:
            view.image = np.dstack((view.image, diff))
        else:
            view.diff = diff
        return view

class GameGammaColorTransform(Transform):
    def __init__(self, transform_dict):
        assert all([isinstance(k, int) for k in transform_dict.keys()])
        #29582 : [1.04, 1.02, 0.93],
        #24651 : [1.05, 1.02, 0.92],
        #30046 : [1.01, 1.01, 1.01]
        self.transform_dict = transform_dict

    def __call__(self, view_key, view):
        if view_key.instant_key.game_id in self.transform_dict.keys():
            gammas = np.array(self.transform_dict[view_key.instant_key.game_id])
            view.image = gamma_correction(view.image, gammas)
        return view

class BayeringTransform(Transform):
    def __init__(self):
        self.R_filter = np.array([[1,0],[0,0]])
        self.G_filter = np.array([[0,1],[1,0]])
        self.B_filter = np.array([[0,0],[0,1]])
    def __call__(self, view_key, view):
        height, width, _ = view.image.shape
        R_mask = np.tile(self.R_filter, [height//2, width//2])
        G_mask = np.tile(self.G_filter, [height//2, width//2])
        B_mask = np.tile(self.B_filter, [height//2, width//2])
        mask = np.stack((R_mask, G_mask, B_mask), axis=2)
        mask = mask[np.newaxis]
        for i, image in enumerate(view.all_images):
            view.all_images[i] = np.sum(image*mask, axis=3)
        view.image = view.all_images[0]

class GameRGBColorTransform(Transform):
    def __init__(self, transform_dict):
        assert all([isinstance(k, int) for k in transform_dict.keys()])
        self.transform_dict = transform_dict

    def __call__(self, view_key: ViewKey, view: View):
        if view_key.instant_key.game_id in self.transform_dict.keys():
            adaptation_vector = np.array(self.transform_dict[view_key.instant_key.game_id])
            view.image = np.clip(view.image.astype(np.float32)*adaptation_vector, 0, 255).astype(np.uint8)
        return view

class ViewRandomCropperTransform(RandomCropperTransform):
    def _apply_transformation(self, view, A):
        if self.debug:
            w, h = self.output_shape
            points = Point2D(np.linalg.inv(A)@Point2D([0,0,w,w],[0,h,h,0]).H)
            cv2.polylines(view.image, [points.T.astype(np.int32)], True, (255,0,0), self.linewidth)
        else:
            view.image = cv2.warpAffine(view.image, A[0:2,:], self.output_shape, flags=cv2.INTER_LINEAR)
            view.calib = view.calib.update(K=A@view.calib.K, width=self.output_shape[0], height=self.output_shape[1])

            if hasattr(view, "all_images"):
                for i in range(1, len(view.all_images)): # skip first image as it was already done
                    view.all_images[i] = cv2.warpAffine(view.all_images[i], A[0:2,:], self.output_shape, flags=cv2.INTER_LINEAR)
            if hasattr(view, "human_masks") and view.human_masks is not None:
                view.human_masks = cv2.warpAffine(view.human_masks, A[0:2,:], self.output_shape, flags=cv2.INTER_NEAREST)
        return view

class NaiveViewRandomCropperTransform(ViewRandomCropperTransform):
    def __init__(self, *args, scale_min=0.5, scale_max=2, **kwargs):
        """ scale is the scale factor that will be applied to images
        """
        super().__init__(*args, size_min=scale_min, size_max=scale_max, **kwargs)

    def _get_current_parameters(self, view_key, view):
        input_shape = view.calib.width, view.calib.height
        return None, 1, input_shape

class CleverViewRandomCropperTransform(ViewRandomCropperTransform):
    def __init__(self, *args, def_min=60, def_max=160, **kwargs):
        """
            def -  definition in pixels per meters. 60px/m = ball of 14px
        """
        super().__init__(*args, size_min=def_min, size_max=def_max, **kwargs)

    def random_ball(self, view_key, view):
        court = setdefaultattr(view, "court", Court(getattr(view, "rule_type", "FIBA")))
        top_edge = list(court.visible_edges(view.calib))[0]
        start = top_edge[0][0][0]
        stop = top_edge[1][0][0]
        x = np.random.beta(2, 2)*(stop-start)+start
        y = np.random.beta(2, 2)*court.h/2+court.h/4
        z = 0
        return Point3D(x,y,z)

    def _get_current_parameters(self, view_key, view):
        keypoints = self.random_ball(view_key, view)
        size = float(view.calib.compute_length2D(100, keypoints))
        keypoints = view.calib.project_3D_to_2D(keypoints)
        input_shape = view.calib.width, view.calib.height
        if self.debug:
            raise NotImplementedError("Selected keypoint should be drawn in view.image (as well as it's projection on court for better visualization)")
        return keypoints, size, input_shape

class BallViewRandomCropperTransform(CleverViewRandomCropperTransform):
    def __init__(self, *args, size_min=None, size_max=None, def_min=None, def_max=None, on_ball=False, **kwargs):
        msg = "Only one of ('size_min' and 'size_max') or ('def_min' and 'def_max') should be defined"
        if size_min is not None and size_max is not None:
            assert def_min is None and def_max is None, msg
            super().__init__(*args, def_min=size_min, def_max=size_max, **kwargs)
            self.true_size = BALL_DIAMETER
        elif def_min is not None and def_max is not None:
            assert size_min is None and size_max is None, msg
            super().__init__(*args, def_min=def_min, def_max=def_max, **kwargs)
            self.true_size = 100

        self.on_ball = {False: 0.5, True: 1.0, None: 0.0}.get(on_ball, on_ball)

    def _get_current_parameters(self, view_key, view):
        balls = [a for a in view.annotations if a.type == "ball" and a.camera == view_key.camera]
        ball = random.sample(balls, 1)[0].center if balls else None

        # If not `on_ball` use the ball anyway half of the samples
        keypoint = ball if random.random() < self.on_ball else self.random_ball(view_key, view)
        if keypoint is None:
            return None

        # Use ball if any, else use the random ball (it only affects the strategy to scale)
        size = float(view.calib.compute_length2D(self.true_size, ball if ball is not None else keypoint))

        keypoints = view.calib.project_3D_to_2D(keypoint)
        input_shape = view.calib.width, view.calib.height
        return keypoints, size, input_shape

class PlayerViewRandomCropperTransform(ViewRandomCropperTransform):
    def __init__(self, output_shape, def_min=60, def_max=160, margin=100, **kwargs):
        """
            def -  definition in pixels per meters. 60px/m = ball of 14px
            margin - a margin in cm the keypoints
        """
        super().__init__(output_shape=output_shape, size_min=def_min, size_max=def_max, **kwargs)
        self.margin = margin

    def focus_on_player(self, view_key, view):
        players = [a for a in view.annotations if a.type == "player" and a.camera == view_key.camera]
        if not players:
            return None
        player = random.sample(players, 1)[0]
        keypoints = Point3D([player.head, player.hips, player.foot1, player.foot2])
        return keypoints

    def _get_current_parameters(self, view_key, view):
        raise NotImplementedError("This code was not tested. Images should be visualized.")
        keypoints = self.focus_on_player(view_key, view)
        if keypoints is None:
            return None
        margin = float(view.calib.compute_length2D(self.margin, Point3D(np.mean(keypoints, axis=1))))
        size = float(view.calib.compute_length2D(100, Point3D(np.mean(keypoints, axis=1))))
        keypoints = view.calib.project_3D_to_2D(keypoints)
        input_shape = view.calib.width, view.calib.height
        return keypoints, size, input_shape

class AddBallSizeFactory(Transform):
    def __call__(self, view_key, view):
        predicate = lambda a: a.camera == view_key.camera and a.type == "ball" and view.calib.projects_in(a.center) and a.visible is not False
        balls = [a.center for a in view.annotations if predicate(a)]
        return {"ball_size": view.calib.compute_length2D(BALL_DIAMETER, Point3D(balls))[0] if balls else np.nan}

class AddBallPositionFactory(Transform):
    def __call__(self, view_key, view):
        return {"ball": view.ball.center}

class AddDiffFactory(Transform):
    def __call__(self, view_key, view):
        return {"input_image2": view.all_images[1]}

class AddCalibFactory(Transform):
    def __init__(self, as_dict=False):
        self.as_dict = as_dict
    @staticmethod
    def to_basic_dict(calib):
        return {
            "K": calib.K,
            "r": cv2.Rodrigues(calib.R)[0].flatten(),
            "T": calib.T,
            "width": np.array([calib.width]),
            "height": np.array([calib.height]),
            "kc": np.array(calib.kc),
        }
    def __call__(self, view_key, view):
        if self.as_dict:
            return self.to_basic_dict(calib)
        return {"calib": view.calib}

class AddCourtFactory(Transform):
    def __call__(self, view_key, view):
        if not getattr(view, "court", None):
            view.court = Court()
        return {
            "court_width": np.array([view.court.w]),
            "court_height": np.array([view.court.h])
        }

class AddImageFactory(Transform):
    def __call__(self, view_key, view):
        return {"input_image": view.image}

class AddHumansSegmentationTargetViewFactory(Transform):
    def __call__(self, view_key, view):
        return {"human_masks": view.human_masks}

class AddBallSegmentationTargetViewFactory(Transform):
    def __call__(self, view_key, view):
        calib = view.calib
        target = np.zeros((calib.height, calib.width), dtype=np.uint8)
        for ball in [a for a in view.annotations if a.type == "ball" and calib.projects_in(a.center) and a.visible]:
            diameter = calib.compute_length2D(BALL_DIAMETER, ball.center)
            center = calib.project_3D_to_2D(ball.center)
            #cv2.circle(target, center.to_int_tuple(), radius=int(diameter/2), color=1, thickness=-1)
            target[skimage.draw.disk(center.flatten()[::-1], radius=float(diameter/2), shape=target.shape)] = 1
        return {
            "target": target
        }

try:
    from calib3d.pycuda import CudaCalib
    import pycuda.driver as cuda
    # pylint: disable=unused-import
    import pycuda.autoinit
    # pylint: enable=unused-import
    from pycuda.compiler import SourceModule

    class AddBallDistance(Transform):
        def __init__(self):
            self._calib_struct_ptr = cuda.mem_alloc(CudaCalib.memsize())
            self._ball_ptr = cuda.mem_alloc(3*8)
            cuda_code = open(os.path.join(os.path.dirname(__file__), "mod_source.c"), "r").read()
            mod = SourceModule(str(CudaCalib.struct_str())+cuda_code)
            self._ball_distance = mod.get_function("BallDistance")
            self._bdim = (32,32,1)

        def __repr__(self):
            return "{}()".format(self.__class__.__name__)

        def __call__(self, key, view: View):
            # copy calib to GPU
            calib = CudaCalib.from_calib(view.calib)
            calib.memset(self._calib_struct_ptr, cuda.memcpy_htod)

            # copy ball position to GPU
            cuda.memcpy_htod(self._ball_ptr, memoryview(view.ball.center))

            # create distmap on GPU
            distmap_gpu = cuda.mem_alloc(calib.img_width * calib.img_height * 8)# 8 bytes per double
            cuda.memset_d8(distmap_gpu, 0, calib.img_width * calib.img_height * 8)

            # compute best block and grid dimensions
            dx, mx = divmod(calib.img_width, self._bdim[0])
            dy, my = divmod(calib.img_height, self._bdim[1])
            gdim = ( (dx + (mx>0)) * self._bdim[0], (dy + (my>0)) * self._bdim[1])

            # call gpu function
            self._ball_distance(distmap_gpu, self._calib_struct_ptr, self._ball_ptr, block=self._bdim, grid=gdim)

            # copy result to memory
            view.ball_distance = np.zeros((calib.img_height,calib.img_width))#, np.int8)
            cuda.memcpy_dtoh(view.ball_distance, distmap_gpu)
            # cuda.Context.synchronize()
            return view
except ModuleNotFoundError as e:
    if e.name == "calib3d.pycuda":
        raise e

except ImportError as e:
    if "CudaCalib" not in str(e.msg):
        raise e
