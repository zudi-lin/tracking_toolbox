import numpy as np
import skvideo.io
from matplotlib import pyplot as plt
from skimage.color import rgb2gray
from skimage.measure import label
from skimage.morphology import remove_small_objects, erosion, dilation, disk
from skimage.filters import gaussian

def find_valid_region(image, thres=32, size_thres=128, show_imgs=False, cropped_as_valid=False):
    """ Calculate the valid region mask of the chamber.
    """
    if cropped_as_valid: # use the region cropped by the user as the valid region
        valid_mask = np.ones(image.shape, dtype=np.uint8)
        valid_mask[0, :] = 0
        valid_mask[:, 0] = 0
        valid_mask[-1, :] = 0
        valid_mask[:, -1] = 0

    else: # calculate the valid region
        image = (image-image.min())/(image.max()-image.min())
        image = (image*255).astype(np.uint8)
        binary = (image < thres).astype(np.uint8)
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

        pos = np.argmax(counts)
        valid_mask = (segmentation==indices[pos]).astype(np.uint8)
        valid_mask = erosion(valid_mask, np.ones((3,3), dtype=np.uint8))

    ycoord, xcoord = np.where(valid_mask==1)
    height = ycoord.max() - ycoord.min()
    width  = xcoord.max() - xcoord.min()
    return valid_mask, height, width
    
def segment_image(image, valid_region, show_imgs=False, thres=128, size_thres=64, 
                  relative_brightness=True, filtering=False):
    """Locate the target animal in each frame by image segmentation
    """
    value_min, value_max = image.min(), image.max()
    image = image * valid_region
    image = np.clip(image, a_min=value_min, a_max=value_max)
    image = (image-image.min())/(image.max()-image.min())
    if filtering:
        image = gaussian(image, sigma=1, preserve_range=True)
    image = (image*255).astype(np.uint8)

    if relative_brightness:
        temp = image.copy()
        temp_thres = (temp.max() + temp.mean()) // 2 
        binary = (image > temp_thres).astype(np.uint8)
    else:
        binary = (image > thres).astype(np.uint8)

    binary = binary * valid_region
    if binary.sum() > size_thres * 2:
        binary = erosion(binary)
    
    segmentation = label(binary)
    if len(np.unique(segmentation))>2 and binary.sum() > size_thres * 2:
        segmentation = remove_small_objects(segmentation, size_thres)
            
    indices, counts = np.unique(segmentation, return_counts=True)
    if len(indices) > 1 and indices[0] == 0:
        indices, counts = indices[1:], counts[1:]
        pos = [np.argmax(counts)]
    else:
        pos = []

    if len(pos)>=1: 
        target_idx = indices[pos[0]]
        target = (segmentation==target_idx).astype(np.uint8)
        if target.sum() > size_thres * 2:
            target = erosion(target)
        foreground_coord = np.where(target!=0)
        # print(foreground_coord)
        center = [int(foreground_coord[0].astype(float).mean()),
                  int(foreground_coord[1].astype(float).mean())]

        if show_imgs:
            plt.figure(figsize=(20,10))

            plt.subplot(141)
            plt.imshow(binary*255, cmap='gray')
            plt.title('binary')
            plt.axis('off')

            plt.subplot(142)
            plt.imshow(segmentation, cmap='tab20c')
            plt.title('segmentation')
            plt.axis('off')

            plt.subplot(143)
            plt.imshow(target, cmap='gray')
            plt.title('target')
            plt.axis('off')

            plt.subplot(144)
            plt.imshow(image, cmap='gray')
            plt.scatter(center[1], center[0], c='r', s=20)
            plt.title('tracking [%d %d]' % (center[1], center[0]))
            plt.axis('off')
            plt.show()
            
    else:
        center = []

        if show_imgs:
            plt.figure(figsize=(20,10))

            plt.subplot(131)
            plt.imshow(image, cmap='gray')
            plt.title('image')
            plt.axis('off')

            plt.subplot(132)
            plt.imshow(binary*255, cmap='gray')
            plt.title('binary')
            plt.axis('off')

            plt.subplot(133)
            plt.imshow(segmentation, cmap='tab20c')
            plt.title('segmentation')
            plt.axis('off')
            plt.show()
    
    return center