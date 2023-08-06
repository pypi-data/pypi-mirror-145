import time
import sys, os
import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
import scipy.stats
import tracemalloc
import umap
import hdbscan
from inspect import Parameter
import weblogo
from weblogo import *

def onehot_enc(row, expected_length=21):
    """Encode the data with one-hot encoding
    Parameter:
    ---------
        row: string
            DNA or RNA sequence for one-hot encoding. 
    ---------

    Retruns:
    --------
        onehot_array: array
            one-hot encoding data 
    """
    enc = OneHotEncoder(dtype=np.int8)
    enc.fit([[i] for i in "ATCGN"])
    seq = [[i] for i in row["seq"].upper().replace("U","T") if len(row["seq"]) == expected_length]
    onehot_array = enc.transform(seq).toarray().reshape(-1)
    return onehot_array

def UMAP(onehot_input, df, parameters):
    """Dimensionality reduction with UMAP

    Parameter:
    ---------
        onehot_input: array
            One-hot encoding data from sequence.
        df: pd.DataFrame
            Sequence in pd.DataFrame format. It will be added two columns named "X" and "Y" as results of UMAP. 
    ---------
    Retruns:
        pd.DataFrame
    --------
    """
    df = df.copy()

    random_state = int(parameters["random_state"])
    init = str(parameters["umap_init"])
    min_dist = float(parameters["min_dist"])
    n_neighbors = int(parameters["n_neighbors"])
    densmap = bool(parameters["densmap"])
    n_jobs = int(parameters["umap_jobs"])

    model = umap.UMAP(init=init, random_state=random_state, n_components=2, min_dist=min_dist, n_neighbors=n_neighbors, verbose=True, densmap=densmap, n_jobs=n_jobs)
    umap_output = model.fit_transform(onehot_input)
    
    df["X"] = umap_output[:, 0]
    df["Y"] = umap_output[:, 1]
    
    del model
    return df

def cluster_HDBSCAN(df, parameters):
    """Clustering UMAP results with HDSCAN

    Parameter:
    ---------
        df: pd.DataFrame
            The results of UMAP computed from UMAP nearst neighbor. After clustering with HDBSCAN, add a columns to it named "Cluster".
        parameters: list
            Parameters for HDBSCAN from user. 
    ---------

    Retruns:
    --------
        pd.DataFrame 
    """
    # use multi-code here
    df = df.copy()
    X = np.stack([df["X"], df["Y"]], axis=1)

    min_cluster_size = int(parameters["min_cluster_size"])
    min_samples = int(parameters["min_samples"])
    cluster_selection_method = str(parameters["cluster_selection_method"])
    core_dist_n_jobs = int(parameters["hdbscan_jobs"])
    cluster_selection_epsilon = float(parameters["cluster_selection_epsilon"])
    if bool(parameters["softclustering"]) == True:
        prediction_data = True
    else:
        prediction_data = False

    model = hdbscan.HDBSCAN(min_cluster_size = min_cluster_size, min_samples=min_samples, cluster_selection_method=cluster_selection_method, cluster_selection_epsilon=cluster_selection_epsilon, core_dist_n_jobs=core_dist_n_jobs, prediction_data=prediction_data)
    if prediction_data == True:
        yhat = model.fit(X)
        soft_clusters = hdbscan.all_points_membership_vectors(yhat)
        labels = [np.argmax(x) for x in soft_clusters] 
    else:
        labels = model.fit_predict(X)
    
    df["Cluster"] = [i+1 if i > -1 else -1 for i in labels ]  # re-number lables to make it human-readable

    # check cluster number
    # print(df.groupby("Cluster")["Cluster"].count())
    return df


def run_cluster(fasta_df, path, parameters):
    """Call two algorithms to cluster and get the result  
    Parameter:
    ---------
        fasta_df: pd.DataFrame
            Sequence file in pd.DataFrame format. After calling two algorithms, add three columns to it named "X", "Y" and "Cluster" to store the results.
        path: str
            The output directory.
        parameters: list
            Parameters for HDBSCAN from user input.

    ---------
    Retruns:
    --------
        pd.DataFrame
    """
    onehot_input = []
    for idx, row in fasta_df.iterrows():
        onehot_input.append(onehot_enc(row, expected_length=int(parameters["exp_len"])))
    onehot_input = np.array(onehot_input)

    df_UMAP = UMAP(onehot_input, fasta_df, parameters)
    df_HDBSCAN = cluster_HDBSCAN(df_UMAP, parameters)
    # print(df_HDBSCAN)
    df_HDBSCAN.to_csv("{path}/all_clusters.csv".format(path=path),index = None)
    
    base_type = parameters["weblogo_base_type"]

    with open("{path}/init.fa".format(path=path), "w") as init_fasta:
        for idx, row in df_HDBSCAN.iterrows():
            if base_type == "DNA":
                seq_out = str(row["seq"]).upper().replace("U", "T")
            elif base_type == "RNA":
                seq_out = str(row["seq"]).upper().replace("T", "U")
            else:
                seq_out = str(row["seq"]).upper()
            init_fasta.write(">{}\n{}\n".format(idx, seq_out))
    return df_HDBSCAN

def draw_logo(infile, parameters):
    """Create sequence logos with Weblogo
    Parameters:
    ---------
        infile: string
            A sequence file in fasta format to create sequence logo with Weblogo.
    ---------
    Returns:
        A picture of sequence logo in png format.
    --------
    """
    
    unit = parameters["weblogo_unit"]
    first_index = int(parameters["weblogo_first_index"])
    
    data = open(infile)
    seqs = read_seq_data(data)

    logodata = LogoData.from_seqs(seqs)
    logooptions = LogoOptions(
        unit_name = unit, # 'probability',
        yaxis_label = unit, # 'probability',
        first_index = first_index, # -10,
        color_scheme = classic,
        resolution = 1000
    )
    logoformat = LogoFormat(logodata,logooptions)
    png = png_print_formatter(logodata,logoformat)

    return png

