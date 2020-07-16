import numpy as np
import skvideo.io
from matplotlib import pyplot as plt
from skimage.color import rgb2gray
from skimage.measure import label
from skimage.morphology import remove_small_objects, erosion, dilation, disk
from skimage.filters import gaussian

def find_valid_region(image, thres=32, size_thres=128, show_imgs=False):
    image = (image-image.min())/(image.max()-image.min())
    image = (image*255).astype(np.uint8)
    binary = (image > thres).astype(np.uint8)
    segmentation = label(binary)
    segmentation = remove_small_objects(segmentation, size_thres)
    indices, counts = np.unique(segmentation, return_counts=True)
    # print(indices, counts)
    
    if show_imgs:
        plt.imshow(image)
        plt.show()
        for i in np.unique(indices):
            temp = (segmentation==i).astype(np.uint8)*255
            plt.imshow(temp)
            plt.title(i)
            plt.show()

    valid_mask = (segmentation==0).astype(np.uint8)
    valid_mask = erosion(valid_mask, np.ones((3,3), dtype=np.uint8))
    return valid_mask
    
def segment_image(image, show_imgs=False, thres=128, size_thres=64, valid_region=None):
    image = (image-image.min())/(image.max()-image.min())
    image = gaussian(image, sigma=1, preserve_range=True)
    image = (image*255).astype(np.uint8)
    binary = (image > thres).astype(np.uint8)
    binary = erosion(binary)
    if valid_region is not None:
        binary = binary * valid_region
    
    segmentation = label(binary)
    if len(np.unique(segmentation))>1:
        segmentation = remove_small_objects(segmentation, size_thres)
            
    indices, counts = np.unique(segmentation, return_counts=True)
    pos = [i for i in range(len(counts)) if counts[i]>200 and counts[i]<1600]
    # print(indices, counts, pos)
    if len(pos)>=1: 
        target_idx = indices[pos[0]]
        target = (segmentation==target_idx).astype(np.uint8)
        target = erosion(target)
        foreground_coord = np.where(target!=0)
        center = [int(foreground_coord[0].astype(float).mean()),
                  int(foreground_coord[1].astype(float).mean())]

        if show_imgs:
            plt.figure(figsize=(20,10))
            plt.subplot(141)
            plt.imshow(binary*255, cmap='gray')
            plt.axis('off')
            plt.subplot(142)
            plt.imshow(segmentation, cmap='tab20c')
            plt.axis('off')
            plt.subplot(143)
            plt.imshow(target, cmap='gray')
            plt.axis('off')
            plt.subplot(144)
            plt.imshow(image, cmap='gray')
            plt.scatter(center[1], center[0], c='r', s=20)
            plt.axis('off')
            plt.show()
            
    else:
        center = []
    
    return center