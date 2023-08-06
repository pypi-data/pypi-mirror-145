import numpy as np
from shapely.geometry import box, Polygon

from calib3d import Calib as Calib3d
from calib3d import Point3D, Point2D, compute_rotation_matrix # pylint: disable=unused-import
from calib3d.draw import visible_segment

class Calib(Calib3d):
    def visible_edge(self, edge):
        return visible_segment(self, edge[0], edge[1])

    def get_region_visible_corners_2d(self, points_3d: Point3D, approximate_curve_by_N_segments=10):
        """Return a list of corner points defining the 2D boundaries of a specific 3D region on the image space

        Args:
            points_3d ([type]): [description]
            approximate_curve_by_N_segments (int, optional): [description]. Defaults to 10.

        Returns:
            List[Tuple(int, int)]: a list of 2D coordinates of the corner points of a specific 3D region on the image space
        """

        # Construct the polygon defining the boundaries of the 3D region and projects it, considering the lens distorsion (3D straight lines might be curves on the image)
        region_3d_coords = points_3d.close().linspace(approximate_curve_by_N_segments+1)
        region_2d_coords = self.project_3D_to_2D(region_3d_coords)
        any_coord_outside_img_boundaries = np.any(region_2d_coords < 0) or \
                                           np.any(region_2d_coords.x >= self.width) or \
                                           np.any(region_2d_coords.y >= self.height)
        if not any_coord_outside_img_boundaries:
            return region_2d_coords

        # Restrict the 2D region polygon to the image space boundaries
        img_corners = box(minx=0, miny=0, maxx=self.width, maxy=self.height)
        region_corners = Polygon([r.to_int_tuple() for r in region_2d_coords])
        region_polygon_restricted_to_img_space = region_corners.intersection(img_corners)

        if region_polygon_restricted_to_img_space:
            return Point2D(np.array(region_polygon_restricted_to_img_space.exterior.coords).T)
        else:
            return Point2D(np.empty(shape=(2, 0), dtype=float))


def rescale_and_recenter(H, nx, ny):
    # TODO: only consider points on the court and 2m above
    # => it's the only usefull area on the recentered and rescaled image

    # See where image corners get displaced
    p = H @ np.transpose(np.array([[0,0,1],[nx,0,1],[nx,ny,1],[0,ny,1]]))

    # Handle projection inversions:
    # Trick (to address issue in KS-US-MARQUETTEBIRD):
    # if inversion occurs, just set point at double the size of the image (because it is just impossible
    # to go up to infinity. This means we will discard all pixels coresponding to the ground below the
    # camera, and also all pixels further below.)
    pnorm=np.zeros((3,4))
    for i in range(4):
        if p[2,i] > 0: # no inversion
            pnorm[:,i] = p[:,i]/p[2,i]
        else: # inversion took place
            ptemp=p[:,i]/p[2,i]
            ptemp[0] = 2*nx if ptemp[0] < 0 else -nx
            ptemp[1] = 3*ny if ptemp[1] < 0 else -ny
            pnorm[:,i] = ptemp

    minx, maxx = np.min(pnorm[0,:]), np.max(pnorm[0,:])
    miny, maxy = np.min(pnorm[1,:]), np.max(pnorm[1,:])

    # Compute scaling matrix that should be applied to keep corners inside the image
    Hscale=np.array([[nx/(maxx-minx),0,1],[0,ny/(maxy-miny),1],[0,0,1]])

    # See where new corners get displaced after rescale
    p = Hscale @ pnorm

    # Handle projection inversions again
    pnorm = np.zeros((3,4))
    for i in range(4):#=1:4
        if p[2,i] > 0: # no inversion
            pnorm[:,i] = p[:,i]/p[2,i]
        else:
            ptemp=p[:,i]/p[2,i]
            ptemp[0] = 2*nx if ptemp[0] < 0 else -nx
            ptemp[1] = 2*ny if ptemp[1] < 0 else -ny
            pnorm[:,i] = ptemp

    minx=np.min(pnorm[0,:])
    miny=np.min(pnorm[1,:])
    Hshift=np.array([[1,0,-minx],[0,1,-miny],[0,0,1]])

    # Combine scaling and shift
    return Hshift@Hscale

def set_z_vanishing_point(P, nx, ny):
    # Compute the rotation that should be applied to have the
    # projection of somebody standing at the center of the image
    # parralel to vertical

    # 2D position of someone at the center of the image
    center = np.array([nx/2,ny/2,1])
    Hg = P[:,[0,1,3]]
    iHg = np.linalg.inv(Hg)
    pos_center = np.matmul(iHg,np.transpose(center))
    pos_center = pos_center/pos_center[2]

    # Projection of the head (180cm) of the person on the image.
    pos_head=np.array([pos_center[0], pos_center[1], -180, 1])
    pos_head_im=P@pos_head
    pos_head_im=pos_head_im/pos_head_im[2]

    # Correction angle
    alpha=np.arctan2(nx/2-pos_head_im[0],ny/2-pos_head_im[1])
    alpha_degres = alpha*180/np.pi # pylint: disable=unused-variable

    # Corrected P matrix (rotation around the center of the image)
    Tmat=np.array([[1,0,nx/2],[0,1,ny/2],[0,0,1]])
    Rot=[[np.cos(alpha),-np.sin(alpha),0],[np.sin(alpha),np.cos(alpha),0],[0,0,1]]
    Rotmat=Tmat@Rot@np.linalg.inv(Tmat)
    P=Rotmat@P

    # Set z vanishing point at infinity
    fact1=P[0,2]/P[1,2]
    fact2=P[2,2]/P[1,2]
    Mat_vert=np.array([[1,-fact1,0],[0,1,0],[0,-fact2,1]])
    newP=Mat_vert@P

    # Compute shear (persons on the same line in the image should have
    # same size projections)
    K=newP[2,0]/newP[2,1]
    shearf=(K*newP[1,1]-newP[1,0])/(newP[0,0]-K*newP[0,1])
    shear=[[1,0,0],[shearf,1,0],[0,0,1]]

    # Rescale and recenter to keep all pixels inside the transformed image
    SSmat=rescale_and_recenter(shear@Mat_vert@Rotmat, nx, ny)

    # Combined transformation
    return SSmat@shear@Mat_vert@Rotmat

def crop_around_center(image, width, height):
    """ Given a NumPy / OpenCV 2 image, crops it to the given width and height,
        around it's centre point
    """

    image_size = (image.shape[1], image.shape[0])
    image_center = (int(image_size[0] * 0.5), int(image_size[1] * 0.5))

    if width > image_size[0]:
        width = image_size[0]

    if height > image_size[1]:
        height = image_size[1]

    x1 = int(image_center[0] - width * 0.5)
    x2 = int(image_center[0] + width * 0.5)
    y1 = int(image_center[1] - height * 0.5)
    y2 = int(image_center[1] + height * 0.5)

    return image[y1:y2, x1:x2]


class PanoramicStitcher():
    def __init__(self, calibs, output_shape, f=1000, target=None):
        w, h = output_shape
        C = calibs[0].C
        R = compute_rotation_matrix(target, C)
        T = -R@C
        K = np.array([[f, 0, w/2],
                      [0, f, h/2],
                      [0, 0,  1 ]])
        self.camera = Calib(K=K, T=T, R=R, width=w, height=h)
        self.calibs = calibs

        self.width, self.height = w, h = self.camera.width, self.camera.height
        points2D = Point2D(np.stack(np.meshgrid(np.arange(w),np.arange(h))).reshape((2,w*h)))
        points3D = self.camera.project_2D_to_3D(points2D, Z=0)

        def lookuptable(calib, points2D, points3D):
            output_indices = np.where(calib.projects_in(points3D))[0] # indices of output pixels that project to calib
            input_indices = calib.project_3D_to_2D(points3D[:,output_indices]).astype(np.int32) # output pixels that project to calib
            return input_indices, output_indices
        self.lookuptables = [lookuptable(calib, points2D, points3D) for calib in self.calibs]

    def __call__(self, images):
        outputs = np.zeros((len(images), self.height*self.width, 3), dtype=np.uint8)
        for output, image, (input_indices, output_indices) in zip(outputs, images, self.lookuptables):
            output[output_indices] = image[input_indices.y, input_indices.x]
        return np.max(outputs.reshape((-1, self.height, self.width, 3)), axis=0)



