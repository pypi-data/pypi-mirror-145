from dataclasses import dataclass
from enum import IntFlag
import io
import os
import random
import struct
import subprocess
from urllib import request

import cv2
import imageio
from matplotlib import pyplot as plt
import m3u8
import numpy as np

from mlworkflow import Dataset, AugmentedDataset, SideRunner, TransformedDataset
from mlworkflow.datasets import batchify
from aleatorpy import pseudo_random

# This object is defined both in here and in dataset-utilities repository
# Any change here should be reported in dataset-utilities as well
class RobustDataset(Dataset):
    """Handles a parent dataset whose `query_item` can return `None`.
    """
    def __init__(self, parent):
        self.parent = parent
    def yield_keys(self):
        return self.parent.keys
    def query_item(self, key, retry=0):
        item = self.parent.query_item(key)
        while item is None and retry:
            item = self.parent.query_item(key)
            retry -= 1
        return item
    def chunkify(self, keys, chunk_size, drop_incomplete=True, retry=0):
        d = []
        for k, v in ((k, v) for k,v in ((k, self.query_item(k, retry=retry)) for k in keys) if v is not None):
            d.append((k, v))
            if len(d) == chunk_size:  # yield complete sublist and create a new list
                yield d
                d = []
        assert drop_incomplete, "not implemented"
    def batches(self, batch_size, keys=None, wrapper=np.array, drop_incomplete=False, retry=0):
        keys = keys or self.keys
        for chunk in self.chunkify(keys, chunk_size=batch_size, drop_incomplete=drop_incomplete, retry=retry):
            keys, batch = list(zip(*chunk)) # transforms list of (k,v) into list of (k) and list of (v)
            yield keys, batchify(batch, wrapper=wrapper)



# This object is defined both in here and in experimentator repository
# Any change here should be reported in experimentator as well
class SubsetType(IntFlag):
    TRAIN = 1
    EVAL  = 2

# This object is defined both in here and in experimentator repository
# Any change here should be reported in experimentator as well
class Subset:
    def __init__(self, name: str, subset_type: SubsetType, dataset: Dataset, keys=None, repetitions=1, desc=None):
        keys = keys if keys is not None else dataset.keys.all()
        assert isinstance(keys, (tuple, list)), f"Received instance of {type(keys)} for subset {name}"
        self.name = name
        self.type = subset_type
        self.dataset = RobustDataset(dataset)
        self._keys = keys
        self.keys = keys
        self.repetitions = repetitions
        self.desc = desc
        self.is_training = self.type == SubsetType.TRAIN
        loop = None if self.is_training else repetitions
        self.shuffled_keys = pseudo_random(evolutive=self.is_training)(self.shuffled_keys)
        self.dataset.query_item = pseudo_random(loop=loop, input_dependent=True)(self.dataset.query_item)

    def shuffled_keys(self): # pylint: disable=method-hidden
        keys = self.keys * self.repetitions
        return random.sample(keys, len(keys)) if self.is_training else keys

    def __len__(self):
        return len(self.keys)*self.repetitions


def gamma_correction(image, gammas=np.array([1.0, 1.0, 1.0])):
    image = image.astype(np.float32)
    image = image ** (1/gammas)
    image = np.clip(image, 0, 255).astype(np.uint8)
    return image


class MergedDataset(Dataset):
    def __init__(self, *ds):
        self.ds = ds
        self.cache = {}
    def yield_keys(self):
        for ds in self.ds:
            for key in ds.yield_keys():
                self.cache[key] = ds
                yield key
    def query_item(self, key):
        return self.cache[key].query_item(key)

class VideoReaderDataset(Dataset):
    cap = None
    def __init__(self, filename, scale_factor=None, output_shape=None):
        assert not scale_factor or not output_shape, "You cannot provide both 'scale_factor' and 'output_shape' arguments."
        self.cap = cv2.VideoCapture(filename)
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        shape = tuple([int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))])
        if scale_factor:
            shape = tuple(int(x*scale_factor) for x in shape)
        elif output_shape:
            shape = output_shape
        self.shape = tuple(x-x%2 for x in shape) # make sure shape is even
    def __del__(self):
        if self.cap is not None:
            self.cap.release()
    def yield_keys(self):
        yield from range(self.frame_count)
    def query_item(self, i):
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, i)
        _, frame = self.cap.read()
        if frame is None:
            return None
        frame = cv2.resize(frame, self.shape)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return frame

class M3u8PlaylistDataset(Dataset):
    def __init__(self, filename, download_folder=None):
        self.playlist = m3u8.load(filename)
        self.download_folder = download_folder
    def yield_keys(self):
        yield from self.playlist.segments
    def query_item(self, key):
        if self.download_folder is not None:
            filename = os.path.join(self.download_folder, os.path.basename(key.uri))
            request.urlretrieve(key.uri, filename)
            return filename
        return key.uri

class VideoFileNameToDatasetReaderTransform():
    def __init__(self, **kwargs):
        self.kwargs = kwargs
    def __call__(self, key, filename):
        return VideoReaderDataset(filename, **self.kwargs)

class VideoFromPlaylistDataset(AugmentedDataset):
    def augment(self, root_key, dataset):
        for key in dataset.yield_keys():
            item = dataset.query_item(key)
            if item is not None:
                yield (root_key, root_key.uri, key), item

def VideoDataset(filename, **kwargs):
    folder = os.path.dirname(filename)
    supported_formats = {
        ".m3u8": lambda name: VideoFromPlaylistDataset(
            TransformedDataset(
                M3u8PlaylistDataset(name, download_folder=folder),
                [VideoFileNameToDatasetReaderTransform(**kwargs)]
            )
        ),
        ".mp4": lambda name: VideoReaderDataset(name, **kwargs) # pylint: disable=unnecessary-lambda
    }
    return supported_formats[os.path.splitext(filename)[1]](filename)


class DatasetSamplerDataset(Dataset):
    def __init__(self, dataset, count):
        self.parent = dataset
        self.keys = random.sample(list(dataset.keys.all()), count)
    def yield_keys(self):
        for key in self.keys:
            yield key
    def query_item(self, key):
        return self.parent.query_item(key)


def concatenate_chunks(output_filename, *chunk_urls):
    side_runner = SideRunner(10)
    for chunk_url in chunk_urls:
        side_runner.run_async(subprocess.run, ["wget", chunk_url])
    side_runner.collect_runs()

    command = [
        'ffmpeg',
        '-y',
        '-protocol_whitelist "concat,file,http,https,tcp,tls"',
        '-i "concat:{}"'.format("|".join([url[url.rfind("/")+1:] for url in chunk_urls])),
        '-c:a copy',
        '-c:v copy',
        '-movflags faststart',
        output_filename
    ]
    os.system(" ".join(command))
    #subprocess.run(command) # For obscure reason, subprocess doesn't work here

@dataclass
class BoundingBox:
    x: int
    y: int
    w: int
    h: int
    @property
    def x_slice(self):
        return slice(int(self.x), int(self.x+self.w), None)
    @property
    def y_slice(self):
        return slice(int(self.y), int(self.y+self.h), None)

    def increase_box(self, max_width, max_height, aspect_ratio=None, margin=0):
        """ Adapt the bounding-box s.t. it
                - is increased by `margin` on all directions
                - lies within the source image of size `max_width`x`max_height`
                - has the aspect ratio given by `aspect_ratio` (if not None)
                - contains the original bounding-box (box is increased if necessary, up to source image limits)
            Arguments:
                max_width (int)      - width of input image
                max_height (int)     - height of input image
                aspect_ratio (float) - output aspect-ratio
                margin (int)         - margin in pixels to be added on 4 sides
            Returns:
                x_slice (slice) - the horizontal slice
                y_slice (slice) - the vertical slice
        """
        top   = max(0, int(self.y-margin))
        bot   = min(max_height, int(self.y+self.h+margin))
        left  = max(0, int(self.x-margin))
        right = min(max_width, int(self.x+self.w+margin))

        if aspect_ratio is None:
            return slice(left, right, None), slice(top, bot, None)

        w = right - left
        h = bot - top
        if w/h > aspect_ratio: # box is wider
            h = int(w/aspect_ratio)
            if h > max_height: # box is too wide
                h = max_height
                w = int(max_height*aspect_ratio)
                left = max_width//2 - w//2
                return slice(left, w, None), slice(0, h, None)
            cy = (bot+top)//2
            if cy + h//2 > max_height: # box hits the top
                return slice(left, right, None), slice(0, h, None)
            if cy - h//2 < 0: # box hits the bot
                return slice(left, right, None), slice(max_height-h, max_height, None)
            return slice(left, right, None), slice(cy-h//2, cy-h//2+h, None)

        if w/h < aspect_ratio: # box is taller
            w = int(h*aspect_ratio)
            if w > max_width: # box is too tall
                w = max_width
                h = int(max_width/aspect_ratio)
                top = max_height//2 - h//2
                return slice(0, w, None), slice(top, top+h, None)
            cx = (left+right)//2
            if cx + w//2 > max_width: # box hits the right
                return slice(max_width-w, max_width, None), slice(top, bot, None)
            if cx - w//2 < 0: # box hits the left
                return slice(0, w, None), slice(top, bot, None)
            return slice(cx-w//2, cx-w//2+w, None), slice(top, bot, None)

        # else: good aspect_ratio
        return slice(left, right, None), slice(top, bot, None)



class BalancedSubest(Subset):
    """
    """
    def __init(self, balancing_attr, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.balancing_attr = balancing_attr
    def shuffled_keys(self):
        # logic
        return None

class VideoMaker():
    format_map = {
        ".mp4": 'MP4V',
        ".avi": 'XVID',
        ".mpeg4": 'H264'
    }
    writer = None
    def __init__(self, filename="output.mp4", framerate=15):
        self.filename = filename
        self.framerate = framerate
        self.fourcc = cv2.VideoWriter_fourcc(*self.format_map[os.path.splitext(filename)[1]])
    def __enter__(self):
        return self
    def __call__(self, image):
        if self.writer is None:
            shape = (image.shape[1], image.shape[0])
            self.writer = cv2.VideoWriter(self.filename, self.fourcc, self.framerate, shape)
        self.writer.write(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.writer:
            self.writer.release()
            self.writer = None
            print("{} successfully written".format(self.filename))
    def __del__(self):
        if self.writer:
            self.writer.release()
            self.writer = None
            print("{} successfully written".format(self.filename))


def blend(image, saliency, alpha=1.0, beta=0.5, gamma=0.0):
    #assert image.dtype == np.uint8 and image.shape[2] == 3
    #assert saliency.dtype == np.uint8

    if len(saliency.shape) == 2 or saliency.shape[2] == 1:
        saliency = np.dstack((saliency, saliency, saliency))
    return cv2.addWeighted(image, alpha, saliency, beta, gamma)

color_cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']
color_cycle_rgb = list(map(lambda color: list(map(lambda c: int(c, 16), [color[1:3], color[3:5], color[5:7]])), color_cycle))

# Image is 2D numpy array, q is quality 0-100
def jpegBlur(im, q):
    buf = io.BytesIO()
    imageio.imwrite(buf,im,format='jpg',quality=q)
    s = buf.getbuffer()
    return imageio.imread(s,format='jpg')

def setdefaultattr(obj, name, value):
    if not hasattr(obj, name):
        setattr(obj, name, value)
    return getattr(obj, name)

def split_equally(d, K):
    """ splits equally the keys of d given their values
        arguments:
            d (dict) - A dict {"label1": 30, "label2": 45, "label3": 22, ... "label<N>": 14}
            K (int)  - The number of split to make
        returns:
            A list of 'K' lists splitting equally the values of 'd':
            e.g. [[label1, label12, label19], [label2, label15], [label3, label10, label11], ...]
            where
            ```
               d["label1"]+d["label12"]+d["label19"]  ~=  d["label2"]+d["label15"]  ~=  d["label3"]+d["label10"]+d["label11]
            ```
    """
    s = sorted(d.items(), key=lambda kv: kv[1])
    f = [{"count": 0, "list": []} for _ in range(K)]
    while s:
        arena_label, count = s.pop(-1)
        index, _ = min(enumerate(f), key=(lambda x: x[1]["count"]))
        f[index]["count"] += count
        f[index]["list"].append(arena_label)
    return [x["list"] for x in f]


class MJPEGReader:
    def __init__(self, filename):
        self.fd = open(f"{filename}.idx", "rb")
        self.cap = cv2.VideoCapture(filename)
        self.header, self.version = struct.unpack("QI", self.fd.read(12))
    def __del__(self):
        if self.cap:
            self.cap.release()
    def __iter__(self):
        return self
    def __next__(self):
        try:
            tvsec, tvusec, offset, frame_idx, other = struct.unpack("IIQII", self.fd.read(24))
        except:
            raise StopIteration  
        found, image = self.cap.read()
        timestamp = round(tvsec*1000+tvusec/1000)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) if image is not None else None
        return timestamp, offset, frame_idx, other, image

