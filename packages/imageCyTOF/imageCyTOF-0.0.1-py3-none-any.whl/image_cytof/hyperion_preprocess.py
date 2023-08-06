import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings


####################### Read data ########################
def cytof_read_data(filename):
    """ Rread cytof data (.txt file) as a dataframe
    
    Inputs:
        filename = full filename of the cytof data
        
    Returns: 
        df_cytof = dataframe of the cytof data
        
    :param filename: str
    :return df_cytof: pandas.core.frame.DataFrame
    """
    df_cytof = pd.read_table(filename)
    return df_cytof


def cytof_preprocess(df):
    """ Preprocess cytof dataframe
        Every pair of X and Y values represent for a unique physical pixel locations in the original image
        The values for Xs and Ys should be continuous integers
        The missing pixels would be filled with 0

    Inputs:
        df = cytof dataframe
        
    Returns:
        df = preprocessed cytof dataframe with missing pixel values filled with 0
        
    :param df: pandas.core.frame.DataFrame
    :return df: pandas.core.frame.DataFrame
    """
    nrow = max(df['Y'].values) + 1
    ncol = max(df['X'].values) + 1
    n = len(df)
    if nrow * ncol > n:
        df2 = pd.DataFrame(np.zeros((nrow * ncol - n, len(df.columns)), dtype=int), columns=df.columns)
        df = pd.concat([df, df2])
    return df


def cytof_check_channels(df, marker_names=None, xlim=None, ylim=None):
    """A visualization function to show different markers of a cytof image
    
    Inputs:
        df           = preprocessed cytof dataframe
        marker_names = marker names to visualize, should match to column names in df (default=None)
        xlim         = x-axis limit of output image (default=None)
        ylim         = y-axis limit of output image (default=None) 
    
    :param df: pandas.core.frame.DataFrame
    :param marker_names: list
    :param xlim: tuple
    :prarm ylim: tuple
    """
    if marker_names is None:
        marker_names = [df.columns[_] for _ in range(6, len(df.columns))]
    nrow = max(df['Y'].values) + 1
    ncol = max(df['X'].values) + 1
    ax_ncol = 5
    ax_nrow = int(np.ceil(len(marker_names)/5))
    fig, axes = plt.subplots(ax_nrow, ax_ncol, figsize=(3*ax_ncol, 3*ax_nrow))
    if ax_nrow == 1:
        axes = np.array([axes])
    for i, _ in enumerate(marker_names):
        _ax_nrow = int(np.floor(i/ax_ncol))
        _ax_ncol = i % ax_ncol
        image = df[_].values.reshape(nrow, ncol)
        image = np.clip(image/np.quantile(image, 0.99), 0, 1)
        axes[_ax_nrow, _ax_ncol].set_title(_)
        if xlim is not None:
            image = image[:, xlim[0]:xlim[1]]
        if ylim is not None:
            image = image[ylim[0]:ylim[1], :]
        im = axes[_ax_nrow, _ax_ncol].imshow(image, cmap="gray")
        fig.colorbar(im, ax=axes[_ax_nrow, _ax_ncol])
    plt.show()


def define_nuclei_channel(df, nuclei_markers, inplace=False):
    """ Combine provided markers to add to the original dataframe a nuclei channel

    Inputs:
        df             = preprocessed cytof dataframe
        nuclei_markers = markers to be combined to define the nuclei
        inplace        = Whether the query should modify the data in place or return a modified copy (default=False)

    :param df: pandas.core.frame.DataFrame
    :param nuclei_markers: list
    :param inplace: bool
    """
    # create a copy of original dataframe
    result = df.copy()
    for i, marker in enumerate(nuclei_markers):
        if i == 0:
            result['nuclei'] = result[marker]
        else:
            result['nuclei'] += result[marker]
    if inplace:
        df._update_inplace(result)
        return None
    else:
        return result

    
def cytof_txt2img(df, marker_names):
    """ Convert from cytof dataframe to d-dimensional image, where d=length of marker names
        Each channel of the output image correspond to the pixel intensity of the corresponding marker
    
    Inputs:
        df           = cytof dataframe
        marker_names = markers to take into consideration
    
    Returns:
        out_img      = d-dimensional image
        
    :param df: pandas.core.frame.DataFrame
    :param marker_names: list
    :return out_img: numpy.ndarray
    """
    nc_in = len(marker_names)
    marker_names = [_ for _ in marker_names if _ in df.columns.values]
    nc = len(marker_names)
    if nc != nc_in:
        warnings.warn("{} markers selected instead of {}".format(nc, nc_in))
    nrow = max(df['Y'].values) + 1
    ncol = max(df['X'].values) + 1
    print("Output image shape: [{}, {}, {}]".format(nrow, ncol, nc))
    out_image = np.zeros([nrow, ncol, nc], dtype=float)
    for _nc in range(nc):
        out_image[..., _nc] = df[marker_names[_nc]].values.reshape(nrow, ncol)
    return out_image


def cytof_merge_channels(im_cytof, channel_ids, quantiles=None, visualize=False):
    """ Merge selected channels (given by "channel_ids") of raw cytof image and generate a RGB image
    
    Inputs: 
        im_cytof    = raw cytof image
        channel_ids = the indices of channels to be shown
        quantiles   = the quantile values for each channels correspond to channels defined by channel_ids (default=None)
        
    Returns:
        merged_im   = channel merged image
        quantiles   = the quantile values for each channels correspond to channels defined by channel_ids 
        
    :param im_cytof: numpy.ndarray
    :param channel_ids: list
    :param quantiles: list
    :return merged_im: numpy.ndarray
    :return quantiles: list
    """
    merged_im = np.zeros((im_cytof.shape[0], im_cytof.shape[1], 3))
    if quantiles is None:
        quantiles = [np.quantile(im_cytof[..., _], 0.99) for _ in channel_ids]

    for _ in range(min(len(channel_ids), 3)):
        merged_im[..., _] = np.clip(im_cytof[..., channel_ids[_]]/quantiles[_], 0, 1) * 255
    
    chs = [[1, 2], [0, 2], [0, 1]]
    chs_id = 0
    while _ < len(channel_ids) - 1:
        _ += 1
        for j in chs[chs_id]:
            merged_im[..., j] += np.clip(im_cytof[..., channel_ids[_]]/quantiles[_], 0, 1) * 255/2
            merged_im[..., j] = np.clip(merged_im[..., j], 0, 255)
        chs_id += 1
    merged_im = merged_im.astype(np.uint8)
    if visualize:
        plt.imshow(merged_im)
        plt.show()
    return merged_im, quantiles



