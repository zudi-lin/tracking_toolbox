"""Utils for data I/O and visualization
"""
import json
import numpy as np
import skvideo.io
from matplotlib import pyplot as plt
from scipy.ndimage import zoom

from skimage.color import rgb2gray
from skimage.measure import label
from skimage.morphology import remove_small_objects, erosion, dilation, disk

global chunks

def show_rand_imgs(data, num=5, cmap=None):
    plt.figure(figsize=(20,5))
    for i in range(num):
        rand_idx = np.random.randint(0, data.shape[0])
        plt.subplot('1%d%d' % (num, i+1))
        plt.imshow(data[rand_idx], cmap=cmap)
        plt.title("Frame %d" % rand_idx)
        plt.axis('off')
    plt.show()

def string2time(timepoint):
    minutes, seconds = timepoint.split(':')
    return int(minutes)*60 + int(seconds)

def center2dist(center1, center2):
    """Calculate the Euclidean distance between two centers.
    """
    dist = np.array(center1) - np.array(center2)
    dist = (dist**2).sum()
    dist = np.sqrt(dist)
    return dist

def trim_video(video, metadata, start=None, end=None):
    """Trim the video (optional).
    """
    frame_rate_max = 60
    frame_rate = int(metadata["video"]['@avg_frame_rate'].split('/')[0])

    # Adjust frame rate based on the video duration.
    if frame_rate > frame_rate_max:
        duration = float(metadata["video"]["@duration"])
        frame_rate = int(round(video.shape[0] / duration))
    print("Total number of frames in this video: ", video.shape[0])
    print("Frame rate of the video: ", frame_rate)

    if start is not None:
        start_frame = string2time(start) * frame_rate
    else:
        start_frame = 0
    if end is not None:
        end_frame = string2time(end) * frame_rate
    else:
        end_frame = video.shape[0]
    end_frame = min(end_frame, video.shape[0])
    trimmed_video = video[start_frame:end_frame]
    return trimmed_video, frame_rate

def downsample_video(video, ratio=1):
    """Downsample the video by the specified ratio.
    """
    print("Reduce the video resolution by %d times." % ratio)
    zoom_factor = (1.0, 1.0/ratio, 1.0/ratio, 1.0)
    video = zoom(video, zoom_factor, order=1)
    return video

def rgb2gray_chunk(chunk):
    return rgb2gray(chunk)

def load_video(filename, subsample=3, start=None, end=None, p=None, 
               num_cores=1, down_ratio=1, animal_color="white"):
    # load data
    video = skvideo.io.vread(filename)
    if animal_color == "black": # invert the color
        video = 255 - video
    metadata = skvideo.io.ffprobe(filename)

    if start is not None or end is not None:
        video, frame_rate = trim_video(video, metadata, start, end)
    if subsample!=1:
        video = video[::subsample]
    if down_ratio!=1:
        video = downsample_video(video, down_ratio)

    if p is not None:
        chunks = np.array_split(video.copy(), num_cores)
        results = p.map(rgb2gray_chunk, chunks)
        video_gray = np.concatenate(results, 0)
    else:
        video_gray = rgb2gray(video)

    print(video.shape, video_gray.shape)
    return video, video_gray, float(frame_rate) / float(subsample)

def save_video(video, video_gray, center_video, output_name="outputvideo.mp4", 
               track=False, frame_rate=15, verbosity=0, show_example=False, animal_color="white"):
    """Save the tracking video.
    """
    print("The tracking video is saved as ", output_name)
    if video.max() < 1.0:
        video = 255-(video*255).astype(np.uint8)
    if animal_color == "black": # invert the color
        video = 255 - video
    dummy = np.zeros(video_gray.shape, dtype=np.uint8)
    
    struct = disk(4)[None,:,:]
    center_video = dilation(center_video, struct)
    center_video = (center_video*255).astype(np.uint8)
    center_video = np.stack([center_video, dummy, dummy], 3)

    if track: 
        center_video = show_track(center_video)
    
    output_video = np.maximum(video, center_video)
    print(output_video.shape)
    if show_example:
        plt.figure(figsize=(20,10))
        plt.subplot(131)
        plt.imshow(video[0])
        plt.subplot(132)
        plt.imshow(video_gray[0], cmap='gray')
        plt.subplot(133)
        plt.imshow(output_video[0])
        plt.show()
    
    outputdict={'-r': str(frame_rate)}
    skvideo.io.vwrite(output_name, output_video, outputdict=outputdict,
                      verbosity=verbosity)

def show_track(center_video):
    output = center_video.copy()
    num_points = 30
    for i in range(1, num_points+1):
        track_new = center_video.copy()[:-i]
        track_new = np.clip(track_new, a_min=0, a_max=255-5*i)
        output[i:] = np.maximum(output[i:], track_new)
    return output