'''iMVP plots

'''

def show_logos_cols(prefix, names=None, cols=3, figsize=(8,8),
                    auto_size=True, auto_width=4, auto_height=1.5,
                    savefig_name=None, dpi=300):
    """This function is used for plot a series of motif logos in PNG format.
   
    Parameters
    ----------
    prefix: str
        The name of output path, required. This function will scan all PNG files in this path.
    names: tuple
        If given, only plot the given file names. Default=None
    cols: int
        The number of columns. Default=3
    figsize: tuple
        The figsize parameter for matplotlib.pyplot.subpolots()
    auto_size: boolean
        If True, ignore figsze and compute the width and height automatically.
    auto_width: float
        The width factor used for auto_size.
    auto_height: float
        The height factor used for auto_size.
    savefig_name: str
        The plot to save, should end with .pdf or .png or ect. If None, figure will not be drawn.
    dpi: int
        The dpi value for the figure.
    Returns
    -------
    matplotlib.axes
    """
    import os
    import matplotlib.pyplot as plt

    file_list = []
    for img in os.listdir(prefix):
        if img.endswith(".png") == False:
            continue
        if names is not None and fn not in names:
            continue
        if os.path.getsize(prefix+"/"+img) == 0:  # empty file, skipped
            continue
        file_list.append(img)
    
    file_list_format = []
    for i in file_list:
        id = int(i.replace("cluster_", "").replace(".png", ""))
        file_list_format.append((i, id))
    file_list_format = sorted(file_list_format, key=lambda x:x[1]) 
    
    if len(file_list_format) % cols == 0:
        rows = len(file_list_format) // cols
    else:
        rows = len(file_list_format) // cols + 1
    if auto_size == False:
        figsize = figsize
    else:
        width = auto_width * cols
        height = auto_height * rows
        figsize = (width, height)
    
    if len(file_list_format) > 1:
        fig, axes = plt.subplots(rows, cols, figsize=figsize)
        for ax, image in zip(*[axes.reshape(-1), file_list_format]):
            fn, id = image
            img = plt.imread(prefix+"/"+fn)
            _ = ax.imshow(img)
            ax.set_title("cluster #{}".format(id))
        for ax in axes.reshape(-1):
            ax.axis("off")
        if savefig_name is not None:
            plt.savefig(savefig_name, dpi=dpi)
        plt.tight_layout()
        return axes
    else:
        fig, ax = plt.subplots(figsize=figsize)
        fn, id = file_list_format[0]
        img = plt.imread(prefix+"/"+fn)
        _ = ax.imshow(img)
        ax.set_title("cluster #{}".format(id),size=16)
        ax.axis("off")
        plt.tight_layout()
        if savefig_name is not None:
            plt.savefig(savefig_name, dpi=dpi)
        return ax
    
def draw_2D_hist(df, vmax=0.05, cmin = None, density = True, 
                 xlim = None, ylim = None,
                 bins = [600, 600]):
    """This function is used for draw a 2D histogram.
   
    Parameters
    ----------
    df: pd.DataFrame
        A DataFrame containing the columns X and Y.
    vmax: float
        The vmax parameter for hist2d. Default=0.05.
    cmin: float
        The cmin parameter for hist2d. Default=None.
    density: boolean
        If draw density histogram. Default=True.
    xlim: tuple
        xlim for hist2d. Default=None.
    ylim: tuple
        ylim for hist2d. Default=None.
    bins: tuple
        Bin numbers for hist2d. Default=[600,600]
    Returns
    -------
    hist2d: np.array
        A 2D array representing the values of the histogram. Please note that this array has been 90-degree rotated to fit the real X-Y and hence can be drawn with plt.imshow() directly.
    edgesX: np.array
        The X edges.
    edgesY: np.array
        The Y edges
    """
    import matplotlib.pyplot  as plt
    import numpy as np
    fig, ax = plt.subplots(figsize=[6,6])
    ax.set_aspect('equal', 'box')
    hist2d, edgesX, edgesY, ax_hist = ax.hist2d(df["X"], df["Y"], range=[xlim, ylim], vmax=vmax, bins=bins, cmin=cmin, density=density)
    
    # small trick here, the x,y row/col is different in figure and numpy, let's make it the same as we view
    hist2d = np.rot90(hist2d)
    
    ax.set_xticks([])
    ax.set_yticks([])
    plt.tight_layout()
    return hist2d, edgesX, edgesY

if __name__ == "__main__":
    pass