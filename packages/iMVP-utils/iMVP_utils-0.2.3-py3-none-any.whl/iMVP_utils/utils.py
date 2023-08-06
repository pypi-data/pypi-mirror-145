"""iMVP helper functions.

"""

def load_sequences_from_fasta(fn):
    """This function is used for load sequences from a FASTA file into a pandas DataFrame.
    
    Parameters
    ----------
    fn: str
        The file to load.
        
    Returns
    -------
    pd.DataFrame
    """
    import pandas as pd
    from Bio import SeqIO
    N = 0
    data = {"seq": {}, "site": {}}
    for seq in SeqIO.parse(fn, "fasta"):
        data["seq"][N] = str(seq.seq)
        data["site"][N] = seq.id
        N += 1
    return pd.DataFrame(data)

def extract_fasta_and_draw_motifs(prefix, df, cluster_col="Cluster", filter=None, motif_column="seq", draw_logos=True):
    """This function is used for quick extraction of sequences strored in a DataFrame into a FASTA file and then draw the motif logos with Weblogo.
   
    Parameters
    ----------
    prefix: str
        The name of output path, required.
    df: pd.DataFrame
        A DataFrame containing the sequences used, required.
    cluster_col: str or tuple
        The column name for the clusters, default="Cluster".
    filter: boolean
        The column name used for filtering results, where only TRUE values will be used, default=None (not applied).
    motif_column: str or tuple
        The column that cotaining the motif sequences, default="motif_F10".
    draw_logos: boolean
        If use Weblogo to draw logos, default=True.
    
    Returns
    -------
    None
    """
    import os
    print("===============  {} ===============".format(prefix))
    if os.path.isdir("{}".format(prefix)) == False:
        os.mkdir("./{}".format(prefix))
        os.mkdir("./{}/fasta".format(prefix))
        os.mkdir("./{}/logos_bits".format(prefix))
        os.mkdir("./{}/logos_bits_no_axis".format(prefix))
        os.mkdir("./{}/logos_freq".format(prefix))
        os.mkdir("./{}/logos_freq_png".format(prefix))
        os.mkdir("./{}/logos_bits_png".format(prefix))
    else:
        os.system("rm -r ./{}/*".format(prefix))
        os.mkdir("./{}/fasta".format(prefix))
        os.mkdir("./{}/logos_bits".format(prefix))
        os.mkdir("./{}/logos_bits_no_axis".format(prefix))
        os.mkdir("./{}/logos_freq".format(prefix))
        os.mkdir("./{}/logos_freq_png".format(prefix))
        os.mkdir("./{}/logos_bits_png".format(prefix))
    if filter is not None:
        df = df[df[filter] == True].copy()
    clusters = set(df[cluster_col].tolist())
    for g in clusters:
        subdf = df[df[cluster_col] == g]
        with open("./{}/fasta/cluster_{}.fa".format(prefix, g), "w") as output:
            N = 0
            for idx, row in subdf.iterrows():
                output.write(">{}\n{}\n".format(idx, row[motif_column].replace("T", "U")))  # to RNA bases
                N += 1
            print("Cluster #{}: {}".format(g, N))
    if draw_logos == True:
        for g in clusters:
            os.system("weblogo -A rna -D fasta -F pdf --resolution 1000 --color-scheme classic --composition none -i -10 -P cluster_{g} -f ./{prefix}/fasta/cluster_{g}.fa > ./{prefix}/logos_bits/cluster_{g}.pdf".format(prefix=prefix, g=g))
            
            os.system("weblogo -A rna -D fasta -F png --resolution 1000 --color-scheme classic --composition none -i -10 -P cluster_{g} -f ./{prefix}/fasta/cluster_{g}.fa > ./{prefix}/logos_bits_png/cluster_{g}.png".format(prefix=prefix, g=g))

            os.system("weblogo -A rna -D fasta -F pdf -y Frequency --resolution 1000 --color-scheme classic --units probability --composition none -i -10 -P cluster_{g} -f ./{prefix}/fasta/cluster_{g}.fa > ./{prefix}/logos_freq/cluster_{g}.pdf".format(prefix=prefix, g=g))
            
            os.system("weblogo -A rna -D fasta -F png -y Frequency --resolution 1000 --color-scheme classic --units probability --composition none -i -10 -P cluster_{g} -f ./{prefix}/fasta/cluster_{g}.fa > ./{prefix}/logos_freq_png/cluster_{g}.png".format(prefix=prefix, g=g)) 
            
            os.system("weblogo -A rna -D fasta -X no -Y no -P \"\" -F pdf --resolution 1000 --color-scheme classic --composition none -i -10 -f ./{prefix}/fasta/cluster_{g}.fa > ./{prefix}/logos_bits_no_axis/cluster_{g}.pdf".format(prefix=prefix, g=g))

def hist_to_spots(hist2d, cutoff = 5, bins=[600, 600],
                 pixel_lower = 1, pixel_upper = 10,
                 show_small_clusters_id=True, show_big_clusters_id=True,
                 figsize=(12,12), figure_name="hist2D.png"):
    """This function is used for converting 2D histogram to spots (clusters).
   
    Parameters
    ----------
    hist2d: str
        The 2D histogram. (From draw_hist2d function)
    cutoff: int
        The cutoff for cv2.threshold, range from 0 to 255. Default=5.
    bins: tuple
        Should be equal to that of the hist2D.
    pixel_lower: int
        The lower limit of the pixels considering as a "small spot". Spots smaller than this will be ignored.
    pixel_upper: int
        The upper limit of the pixels considering as a "small spot". Spots larger than this will be considered as "big spot"
    show_small_clusters_id: boolean
        If draw the ids for small clusters.
    show_big_clusters_id: boolean
        If draw the ids for big clusters.
    figsize: tuple
        Figure size for matplotlib.
    figure_name: str
        The name of hist2D figure.
    Returns
    -------
    axes: matplotlib.axes
        The axes.
    dict_cnt_small:
        A dictionary of {id: locations} for the small spots.
    dict_cnt_big
        A dictionary of {id: locations} for the big spots.
    """

    import numpy as np
    import matplotlib.pyplot as plt
    import cv2
    from collections import defaultdict

    hist2d = hist2d.copy()
    cutoff = int(cutoff)

    hist2d = hist2d/(hist2d.max()/255.0)
    hist2d = hist2d.astype('uint8')
    hist2d_raw = hist2d.copy()
    
    thresh = cv2.threshold(hist2d, cutoff, 255, cv2.THRESH_BINARY)[1]
   
    thresh_small = hist2d_raw.copy()
    thresh_small[thresh_small>cutoff] = 0
    thresh_small[thresh_small>0] = 255
    
    contours, _ = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE) # 
    contours_filtered_small = []
    contours_filtered_big = []
    dropped = []
    
    N = 0
    show_contours_small =np.zeros(bins).astype('uint8')
    show_contours_big =  np.zeros(bins).astype('uint8')
    dict_cnt_big = defaultdict(list)
    dict_cnt_small = defaultdict(list)
    
    mask =np.zeros(bins).astype('uint8')
    stistics = {"big_pixels":0, "big_cnt": 0, "small_pixels":0, "small_cnt":0, "ignored_pixels":0, "ignored_cnt":0}
    for cnt in contours:
        if pixel_lower <cv2.contourArea(cnt)< pixel_upper:
            contours_filtered_small.append(cnt)
            cimg = np.zeros(bins).astype('uint8')
            cv2.drawContours(cimg, [cnt], -1, 255, -1)
            cimg_rot90 = np.rot90(cimg, k = 1)
            pts = np.where(cimg_rot90 == 255)
            stistics["small_cnt"] += 1
            for i,j in zip(*pts):
                # c = hist2d_raw[i, j]
                stistics["small_pixels"] += 1
                dict_cnt_small[int(stistics["small_cnt"])].append((bins[0]-i, j))
        elif cv2.contourArea(cnt) >= pixel_upper:
            contours_filtered_big.append(cnt)
            cimg = np.zeros(bins).astype('uint8')
            cv2.drawContours(cimg, [cnt], -1, 255, -1)
            cimg_rot90 = np.rot90(cimg)
            pts = np.where(cimg_rot90 == 255)
            stistics["big_cnt"] += 1
            for i,j in zip(*pts):
                # c = hist2d_raw[i, j]
                stistics["big_pixels"] += 1
                dict_cnt_big[stistics["big_cnt"]].append((bins[0]-i, j))
        else:
            dropped.append(cnt)
            for item in cnt:
                stistics["ignored_cnt"] += 1
                for x,y in item:
                    c = hist2d_raw[x, y]
                    stistics["ignored_pixels"] += c
                        
    print("Pixels ignored: {} pixels in {} cntours".format(stistics["ignored_pixels"], stistics["ignored_cnt"]))
    print("Big contours: {} pixels in {} cntours".format(stistics["big_pixels"], stistics["big_cnt"]))
    print("Small contour: {} piexels in {} cntours".format(stistics["small_pixels"], stistics["small_cnt"]))
    image = cv2.bitwise_and(thresh, thresh, mask=mask)

    cv2.drawContours(show_contours_small, contours_filtered_small, -1, 255, -1)
    cv2.drawContours(show_contours_big, contours_filtered_big, -1, 255, -1)
    cv2.drawContours(thresh_small, dropped, -1, 255, -1)

    fig, axes = plt.subplots(2,2, sharex=True, sharey=True,figsize=figsize)
    axes[0][0].imshow(thresh_small)
    axes[0][1].imshow(show_contours_small)
    axes[1][0].imshow(show_contours_big)
    axes[1][1].imshow(thresh)
    axes[0][0].set_title("Ignored pixels")
    axes[0][1].set_title("Small clusters")
    axes[1][0].set_title("Big clusters")
    axes[1][1].set_title("Thresh")
    axes[0][0].set_xticks([]) # 
    axes[0][0].set_yticks([]) #
    
    if show_big_clusters_id == True:
        for id, xy in dict_cnt_big.items():
            Xs = []
            Ys = []
            for x, y in xy:
                Xs.append(x)
                Ys.append(y)
            c_X = np.mean(Xs)
            c_Y = np.mean(Ys)
            
            diameter_X = np.max(Xs) - np.min(Xs)
            diameter_Y = np.max(Ys) - np.min(Ys)
            
            if diameter_X * diameter_Y >= 250:
                color = "red"
            else:
                color = "white"
            axes[1][0].annotate(str(id), xy=(c_X, c_Y), c=color, ha="center", va="center") 
    
    if show_small_clusters_id == True: 
        for id, xy in dict_cnt_small.items():
            Xs = []
            Ys = []
            for x, y in xy:
                Xs.append(x)
                Ys.append(y)
            c_X = np.mean(Xs)
            c_Y = np.mean(Ys)
            
            diameter_X = np.max(Xs) - np.min(Xs)
            diameter_Y = np.max(Ys) - np.min(Ys)
            
            if diameter_X * diameter_Y >= 250:
                color = "red"
            else:
                color = "white"
            axes[0][1].annotate(str(id), xy=(c_X, c_Y), c=color, ha="center", va="center") 
            
    plt.tight_layout()
    plt.savefig(figure_name, dpi=300)
    return axes, dict_cnt_small, dict_cnt_big

def retrive_clusters(df, edgesX, edgesY, dict_clusters, bins=[600,600], cluster_ids=None, spot_name="spot"):
    """This function is used for annotate sites with clusters.
   
    Parameters
    ----------
    df: pd.DataFrame
        A DataFrame object with X and Y column.
    edgesX: np.array
        The array of X edges generated by hist2D.
    edgesY: np.array
        The array of Y edges generated by hist2D.
    dict_clusters: dict
        The dictionary generated by hist_to_spots.
    bins: tuple
        Should equal to that of hist2D.
    cluster_ids: iterable
        If given, only find clusters with that ids.
    spot_name: str
        The column name of the clusters.
    Returns
    -------
    pd.DataFrame
    """
    import sys

    df = df.copy()
    indexes = []
    spots  = []
    N = 0
    M = 0
    S = 0
    for spot_id, xy in dict_clusters.items():
        if cluster_ids is None or spot_id in cluster_ids:
            N += 1
            for x, y in xy:
                left = edgesX[x]
                right = edgesX[x+1]
                bottom = edgesY[bins[1]-y-1]
                top = edgesY[bins[1]-y]
                slice = df.loc[(df["X"]>left)& (df["X"]<=right) & (df["Y"]>bottom) & (df["Y"]<=top)]
                indexes.extend(slice.index.tolist())
                spots.extend([spot_id] * slice.shape[0])
                M += 1
                S += slice.shape[0]
                sys.stdout.write("Number of spots: {}, Total pixels:{}, Total sites: {}\r".format(N, M, S))
    df.loc[indexes, "Spot_name"] = spot_name
    df.loc[indexes, "Spot_id"] = spots
    return df

def prepare_kmers_dict(df, column="motif_F14"):
    """Prepare all kmers from a DataFrame with flanking 14 nt sequences.
   
    Parameters
    ----------
    df: pd.DataFrame
        A DataFrame object with X and Y column.
    column: str
        The name of column containing flanking 14 nt sequences.
    Returns
    -------
    dict
    """
    import pandas as pd
    dict_all_5mers = {-4: {}, -3: {}, -2: {}, -1: {}, 0: {}, 1: {}, 2: {}, 3: {}, 4: {}}
    indexes = []
    
    for idx, row in df.iterrows():
        seq = str(row[column]).upper()
        if  len(seq) != 29:
            continue
        for i in range(0, 9):
            kmers_id = i - 4
            dict_all_5mers[kmers_id][idx] = seq[i: i+21]
    return dict_all_5mers

def phase_shift(df, dict_all_5mers, cluster_id=None, column_motif_F10="motif_F10", current_phase=0, target_base="A"):
    """Perform phase shift.
   
    Parameters
    ----------
    df: pd.DataFrame
        A DataFrame object with X and Y column.
    dict_all_5mers: dict
        The dictionary from prepare_kmers_dict.
    cluster_id: int
        The id of specific cluster.
    column_motif_F10: str
        The column name of the 10-nt flanking sequences.
    current_phase: int
        The current phase of the cluster.
    target_base: str
        The target base to perform phase matching.
    Returns
    -------
    pd.DataFrame
    """
    df = df.copy()
    indexes = []
    shifted_seq = []
    for idx, row in df.iterrows():
        if row["Cluster"]==cluster_id and row["Center_base"]!=target_base:
            if row[column_motif_F10][10] != target_base and row[column_motif_F10][10+current_phase] == target_base:
                indexes.append(idx)
                shifted_seq.append(dict_all_5mers[current_phase][idx])
    df.loc[indexes, "Phase_shift"] = current_phase
    df.loc[indexes, column_motif_F10] = shifted_seq
    df.loc[indexes, "Center_base"] = target_base
    return df

if __name__ == "__main__":
    pass