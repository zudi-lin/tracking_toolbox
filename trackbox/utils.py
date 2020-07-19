"""Utils for data I/O and visualization
"""
import json
import numpy as np
import skvideo.io
from matplotlib import pyplot as plt
from skimage.color import rgb2gray
from skimage.measure import label
from skimage.morphology import remove_small_objects, erosion, dilation, disk

def show_rand_imgs(data, num=5, cmap=None):
    plt.figure(figsize=(20,5))
    for i in range(num):
        rand_idx = np.random.randint(0, data.shape[0])
        plt.subplot('1%d%d' % (num, i+1))
        plt.imshow(data[rand_idx], cmap=cmap)
        plt.axis('off')
    plt.show()

def string2time(timepoint):
    minutes, seconds = timepoint.split(':')
    return int(minutes)*60 + int(seconds)

def center2dist(center1, center2):
    # Euclidean distance between two centers 
    dist = np.array(center1) - np.array(center2)
    dist = (dist**2).sum()
    dist = np.sqrt(dist)
    return dist

def trim_video(video, metadata, start=None, end=None):
    frame_rate = int(metadata["video"]['@avg_frame_rate'].split('/')[0])
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

def load_video(filename, subsample=3, start=None, end=None):
    # load data
    video = skvideo.io.vread(filename)
    metadata = skvideo.io.ffprobe(filename)
    if start is not None or end is not None:
        video, frame_rate = trim_video(video, metadata, start, end)
    if subsample!=1:
        video = video[::subsample]
    video_gray = rgb2gray(video)
    print(video.shape, video_gray.shape)
    return video, video_gray, float(frame_rate) / float(subsample)

def save_video(video, video_gray, center_video, output_name="outputvideo.mp4", 
               track=False, frame_rate=15, verbosity=1):
    video = 255-(video*255).astype(np.uint8)
    dummy = np.zeros(video_gray.shape, dtype=np.uint8)
    
    struct = disk(4)[None,:,:]
    center_video = dilation(center_video, struct)
    center_video = (center_video*255).astype(np.uint8)
    center_video = np.stack([center_video, dummy, dummy], 3)

    if track: 
        center_video = show_track(center_video)
    
    output_video = np.maximum(video, center_video)
    print(output_video.shape)
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