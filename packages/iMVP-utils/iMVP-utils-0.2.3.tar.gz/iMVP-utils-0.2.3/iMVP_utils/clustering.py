def run_HDBSCAN(df=None, X=None, Y=None, soft_clustering=True, min_cluster_size=100, min_samples=10,
                cluster_selection_epsilon=0.0, cluster_selection_method='eom',
                draw_condensed_tree=True, core_dist_n_jobs=6):
    """An implement of HDBSCAN (CPU version)
   
    Parameters
    ----------
    df: pd.DataFrame
        A DataFrame with columns X and Y.
    X: iterable
        A list of X values.
    Y: iterable
        A list of Y values.
    soft_clustering: boolean
        Use soft clustering or not. Default=True.
    min_cluster_size: int
        min_cluster_size in HDBSCAN.
    min_samples: int
        min_samples in HDBSCAN
    cluster_selection_epsilon: float
        cluster_selection_epsilon in HDBSCAN
    cluster_selection_method: str
        cluster_selection_method in HDBSCAN. Should be "eom" or "leaf".
    draw_condensed_tree: boolean
        Draw the condensed tree of HDBSCAN or not.
    core_dist_n_jobs:
        core_dist_n_jobs in HDBSCAN.
    Returns
    -------
    sequences_onehot: list
        A list of one-hot encoded sequences.
    """
    import numpy as np
    import hdbscan
    from collections import Counter
    import matplotlib.pyplot as plt
    import seaborn as sns

    if df is None and X is None and Y is None:
        raise ValueError("Please provide a DataFrame or a paired X and Y!")
    if df is not None:
        df = df.copy()
        INPUT = np.stack([df["X"], df["Y"]], axis=1)
    
    if soft_clustering == True:
        model = hdbscan.HDBSCAN(min_cluster_size=min_cluster_size, min_samples=min_samples, cluster_selection_epsilon=cluster_selection_epsilon, cluster_selection_method=cluster_selection_method, core_dist_n_jobs=core_dist_n_jobs, prediction_data=True)
        yhat = model.fit(INPUT)
        soft_clusters = hdbscan.all_points_membership_vectors(yhat)
        labels = [np.argmax(x) for x in soft_clusters] 
    else:
        model = hdbscan.HDBSCAN(min_cluster_size=min_cluster_size, min_samples=min_samples, cluster_selection_epsilon=cluster_selection_epsilon, cluster_selection_method=cluster_selection_method, core_dist_n_jobs=core_dist_n_jobs, prediction_data=False)
        labels = model.fit_predict(INPUT)
    
    clusters = [i+1 if i > -1 else -1 for i in labels ]  # re-number lables to make it human-readable
    print("HDBSCAN cluster number: {}".format(np.max(clusters)))

    if draw_condensed_tree == True:
        fig, ax = plt.subplots()
        model.condensed_tree_.plot(select_clusters=True, selection_palette=sns.color_palette())
        plt.savefig("Condensed_tree.pdf")

    if df is not None:
        df["Cluster"] = clusters
        print(df.groupby("Cluster")["Cluster"].count())
        return df, model
    else:
        for i, j in Counter(clusters).items():
            print(i, j)
        return clusters, model

def run_HDBSCAN_GPU(df=None, X=None, Y=None, min_cluster_size=100, min_samples=10,
                cluster_selection_epsilon=0.0, cluster_selection_method='eom'
                ):
    """An implement of HDBSCAN (GPU version). Only standard clustering mode is available.
   
    Parameters
    ----------
    df: pd.DataFrame
        A DataFrame with columns X and Y.
    X: iterable
        A list of X values.
    Y: iterable
        A list of Y values.
    min_cluster_size: int
        min_cluster_size in HDBSCAN.
    min_samples: int
        min_samples in HDBSCAN
    cluster_selection_epsilon: float
        cluster_selection_epsilon in HDBSCAN
    cluster_selection_method: str
        cluster_selection_method in HDBSCAN. Should be "eom" or "leaf".

    Returns
    -------
    sequences_onehot: list
        A list of one-hot encoded sequences.
    """
    import numpy as np
    import cuml
    from collections import Counter
    import matplotlib.pyplot as plt

    if df is None and X is None and Y is None:
        raise ValueError("Please provide a DataFrame or a paired X and Y!")
    if df is not None:
        df = df.copy()
        INPUT = np.stack([df["X"], df["Y"]], axis=1)

    model = cuml.HDBSCAN(min_cluster_size=min_cluster_size, min_samples=min_samples, cluster_selection_epsilon=cluster_selection_epsilon, cluster_selection_method=cluster_selection_method, prediction_data=False)
    labels = model.fit_predict(INPUT)
    
    clusters = [i+1 if i > -1 else -1 for i in labels ]  # re-number lables to make it human-readable
    print("HDBSCAN cluster number: {}".format(clusters.max()))

    if df is not None:
        df["Cluster"] = clusters
        print(df.groupby("Cluster")["Cluster"].count())
        return df, model
    else:
        for i, j in Counter(clusters).items():
            print(i, j)
        return clusters, model

def run_HDBSCAN_subclustering(df=None, target=None, cluster_col="Cluster", soft_clustering=True,
                min_cluster_size=100, min_samples=10,
                cluster_selection_epsilon=0.0, cluster_selection_method='eom',
                draw_condensed_tree=True, core_dist_n_jobs=None):
    """An implement of HDBSCAN (CPU version) for further clustering of a subcluster.
   
    Parameters
    ----------
    df: pd.DataFrame
        A DataFrame with columns X, Y, and clusters.
    soft_clustering: boolean
        Use soft clustering or not. Default=True.
    min_cluster_size: int
        min_cluster_size in HDBSCAN.
    min_samples: int
        min_samples in HDBSCAN
    cluster_selection_epsilon: float
        cluster_selection_epsilon in HDBSCAN
    cluster_selection_method: str
        cluster_selection_method in HDBSCAN. Should be "eom" or "leaf".
    draw_condensed_tree: boolean
        Draw the condensed tree of HDBSCAN or not.
    core_dist_n_jobs:
        core_dist_n_jobs in HDBSCAN.
    Returns
    -------
    sequences_onehot: list
        A list of one-hot encoded sequences.
    """
    import numpy as np
    import hdbscan
    from collections import Counter
    import matplotlib.pyplot as plt
    import seaborn as sns

    df = df.copy()
    max_cluster_id = df[cluster_col].max()
    
    df1 = df[df[cluster_col]==target].copy()
    
    X = np.stack([df1["X"], df1["Y"]], axis=1)
    
    model = hdbscan.HDBSCAN(min_cluster_size=min_cluster_size, min_samples=min_samples, cluster_selection_method=cluster_selection_method, cluster_selection_epsilon=cluster_selection_epsilon, core_dist_n_jobs=core_dist_n_jobs, prediction_data=True)
    yhat = model.fit(X)
    
    soft_clusters = hdbscan.all_points_membership_vectors(yhat)
    labels = [np.argmax(x) for x in soft_clusters] 

    df1[cluster_col] = [max_cluster_id + i + 1 for i in labels ]  # re-number lables to make it human-readable
    df.loc[df1.index, cluster_col] = df1[cluster_col].tolist()

    print("HDBSCAN cluster number: {}".format(df["Cluster"].max()-1))
    print(df.groupby(cluster_col)[cluster_col].count())

    if draw_condensed_tree == True:
        fig, ax = plt.subplots()
        model.condensed_tree_.plot(select_clusters=True, selection_palette=sns.color_palette())
        plt.savefig("Condensed_tree_subcluster.pdf")
    return df, model

def run_Louvain(graph, df=None, random_state=42, resolution_parameter=1.0):
    """Clustering UMAP result with Louvain.
   
    Parameters
    ----------
    graph: iGraph object
        An iGraph object computed from UMAP nearest neighbor.
    df: pd.DataFrame
        If given, will add a column named "Cluster" to the DataFrame; else will return the labels.
    random_state: int
        Random seed.
    resolution_parameter: float
        resolution_parameter for Louvain
    
    Returns
    -------
    pd.DataFrame or a list
    """

    import louvain
    import numpy as np

    partition_type = louvain.RBConfigurationVertexPartition
    model = louvain.find_partition(graph, partition_type, seed=random_state, resolution_parameter=resolution_parameter)
    labels = np.array(model.membership)
    
    if df is not None:
        df = df.copy()
        df["Cluster"] = labels
        return df
    else:
        return labels

def run_Leiden(graph, df=None, random_state=42, resolution_parameter=1.0):
    """Clustering UMAP result with Leiden.
   
    Parameters
    ----------
    graph: iGraph object
        An iGraph object computed from UMAP nearest neighbor.
    df: pd.DataFrame
        If given, will add a column named "Cluster" to the DataFrame; else will return the labels.
    random_state: int
        Random seed.
    resolution_parameter: float
        resolution_parameter for Louvain
    
    Returns
    -------
    pd.DataFrame or a list
    """

    import leidenalg
    import numpy as np

    partition_type = leidenalg.RBConfigurationVertexPartition
    model = leidenalg.find_partition(graph, partition_type, seed=random_state, resolution_parameter=resolution_parameter)
    labels = np.array(model.membership)
    
    if df is not None:
        df = df.copy()
        df["Cluster"] = labels
        return df
    else:
        return labels

if __name__ == "__main__":
    pass