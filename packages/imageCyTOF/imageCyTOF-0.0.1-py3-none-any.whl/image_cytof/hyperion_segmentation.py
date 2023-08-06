import scipy
import skimage
from skimage import feature
from segmentation_functions import generate_mask, normalize
import numpy as np
import matplotlib.pyplot as plt


def cytof_nuclei_segmentation(im_nuclei, show_process=False, size_hole=50, size_obj=7):
    """ Segment nuclei based on the input nuclei image
    
    Inputs:
        im_nuclei    = raw cytof image correspond to nuclei, size=(h, w)
        show_process = flag of whether show the process  (default=False)
        size_hole    = size of the hole to be removed (default=50)
        size_obj     = size of the small objects to be removed (default=7)
    
    Returns:
        labels       = nuclei segmentation result, where background is represented by 1, size=(h, w)
        
    :param im_nuclei: numpy.ndarray    
    :param show_process: bool
    :param size_hole: int 
    :param size_obj: int
    :return labels: numpy.ndarray
    """
    mask = generate_mask(np.clip(im_nuclei, 0, np.quantile(im_nuclei, 0.95)), fill_hole=False, use_watershed=False)
    mask = skimage.morphology.remove_small_holes(mask.astype(bool), size_hole)
    mask = skimage.morphology.remove_small_objects(mask.astype(bool), size_obj)
    if show_process:
        plt.figure(figsize=(8, 8))
        plt.imshow(mask[0:150, 0:150], cmap='gray')
        plt.show()

    # Find and count local maxima
    distance = scipy.ndimage.distance_transform_edt(mask)
    distance = scipy.ndimage.gaussian_filter(distance, 1)
    local_maxi = skimage.feature.peak_local_max(distance, exclude_border=False, min_distance=2,
                                                indices=False, labels=None)
    markers = scipy.ndimage.label(local_maxi)[0]
    markers = markers > 0
    markers = skimage.morphology.dilation(markers, skimage.morphology.disk(2))
    markers = skimage.morphology.label(markers)
    markers[markers > 0] = markers[markers > 0] + 1
    markers = markers + skimage.morphology.erosion(1 - mask, skimage.morphology.disk(2))

    # Another watershed
    gradient = skimage.filters.rank.gradient(normalize(np.clip(im_nuclei, 0, np.quantile(im_nuclei, 0.95))),
                                             skimage.morphology.disk(3))
    labels = skimage.morphology.watershed(gradient, markers)
    labels = skimage.morphology.closing(labels)

    if show_process:
        fig, axes = plt.subplots(3, 2, figsize=[16, 24], sharex=False, sharey=False)
        ax = axes.ravel()
        ax[0].set_title("HE channel")
        ax[0].imshow(np.clip(im_nuclei[0:150, 0:150], 0, np.quantile(im_nuclei, 0.95)), interpolation='nearest')
        ax[1].set_title("markers")
        ax[1].imshow(markers[0:150, 0:150], cmap=plt.cm.nipy_spectral, interpolation='nearest')
        ax[2].set_title("distance")
        ax[2].imshow(-distance[0:150, 0:150], cmap=plt.cm.nipy_spectral, interpolation='nearest')
        ax[3].set_title("gradient")
        ax[3].imshow(gradient[0:150, 0:150], interpolation='nearest')
        ax[4].set_title("Watershed Labels")
        ax[4].imshow(labels[0:150, 0:150], cmap=plt.cm.nipy_spectral, interpolation='nearest')
        ax[5].set_title("Watershed Labels")
        ax[5].imshow(labels, cmap=plt.cm.nipy_spectral, interpolation='nearest')
        plt.show()

    return labels


def cytof_cell_segmentation(nuclei_seg, radius=10, show_process=False):
    """ Segment cells based on nuclei segmentation result
    
    Inputs: 
        nuclei_seg   = binary image containing nuclei segmentation information, where background is represented by 1.
                     size=(h,w), typically output of the cytof_nuclei_segmentation function
        radius       = assumed radius of cell in pixels (default=10)
        show_process = flag of whether show the process (default=False)
    
    Returns:
        labels       = cell segmentation result, where background is represented by 1, size=(h, w)  
        
    :param nuclei_seg: numpy.ndarray 
    :param radius: int
    :param show_process: bool    
    :return labels: numpy.ndarray
    """

    markers = nuclei_seg.copy()
    mask = nuclei_seg > 1
    unknown = mask.copy()
    unknown = np.logical_xor(skimage.morphology.dilation(unknown, skimage.morphology.disk(5)), mask)
    markers[unknown] = 0
    if show_process:
        plt.figure(figsize=(18, 6))
        plt.subplot(131)
        plt.title('cytoplasm')
        plt.imshow(unknown[0:150, 0:150], cmap=plt.cm.nipy_spectral, interpolation='nearest')

    # watershed
    labels = skimage.morphology.watershed(np.zeros_like(markers), markers)
    if show_process:
        plt.subplot(132)
        plt.title('nuclei')
        plt.imshow(nuclei_seg[0:150, 0:150], cmap=plt.cm.nipy_spectral, interpolation='nearest')
        plt.subplot(133)
        plt.title('cells')
        plt.imshow(labels[0:150, 0:150], cmap=plt.cm.nipy_spectral, interpolation='nearest')
        plt.show()
    return labels
