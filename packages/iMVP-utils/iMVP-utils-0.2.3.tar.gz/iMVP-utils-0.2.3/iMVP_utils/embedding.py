def onehot_encoder_df(df, column="seq", enc_bases="ATCGN"):
    """This function is used for generate One-Hot encoding sequences from a DataFrame.
   
    Parameters
    ----------
    df: pd.DataFrame
        A DataFrame.
    column: str or tuple
        The column containing the sequences
    enc_bases: str
        The encoding bases. Default="ATCGN".

    Returns
    -------
    sequences_onehot: list
        A list of one-hot encoded sequences.
    """
    from sklearn.preprocessing import OneHotEncoder
    import numpy as np
    enc = OneHotEncoder(dtype=np.int8)
    enc.fit([[i] for i in enc_bases])
    
    sequences_onehot = []
    for idx, row in df.iterrows():
        seq = [[i] for i in str(row[column]).upper()]
        sequences_onehot.append(enc.transform(seq).toarray().reshape(-1))
    return sequences_onehot

def onehot_encoder_iterable(iter_obj, enc_bases="ATCGN"):
    """This function is used for generate One-Hot encoding sequences from a iterable object.
   
    Parameters
    ----------
    iter_obj: iterable
        An iterable object containing the sequences.
    enc_bases: str
        The encoding bases. Default="ATCGN".
    Returns
    -------
    sequences_onehot: list
        A list of one-hot encoded sequences.
    """
    from sklearn.preprocessing import OneHotEncoder
    import numpy as np
    enc = OneHotEncoder(dtype=np.int8)
    enc.fit([[i] for i in enc_bases])
    
    sequences_onehot = []
    for item in iter_obj:
        seq = [[i] for i in item.upper()]
        sequences_onehot.append(enc.transform(seq).toarray().reshape(-1))
    return sequences_onehot

def run_UMAP(onehot_input, df=None, init="random", random_state=42, min_dist=0.01, n_neighbors=20, densmap=False, verbose=True, n_jobs=6):
    """An implement of UMAP (CPU version).
   
    Parameters
    ----------
    onehot_input: iterable.
        A list of one-hot encoded sequences.
    df: pd.DataFrame
        A DataFrame to process. If given, it will return a DataFrame with X and Y columns. If not, it will return X and Y, separatively.
    init: str.
        init value for UMAP.
    random_state: int
        random seed.
    min_dist: float
        min_dist for UMAP
    n_neighbors: int
        n_neighbors for UMAP
    densmap: boolean
        If use DensMAP.
    verbose: boolean
        verbose level

    Returns
    -------
    A DataFrame or [X and Y]
    """
    import umap
   
    model = umap.UMAP(init=init, random_state=random_state, n_components=2, min_dist=min_dist, n_neighbors=n_neighbors, verbose=verbose, densmap=densmap, n_jobs=n_jobs)
    umap_output = model.fit_transform(onehot_input)
    
    if df is not None:
        df = df.copy()
        df["X"] = umap_output[:, 0]
        df["Y"] = umap_output[:, 1]
        del model
        return df
    else:
        del model
        return umap_output[:, 0], umap_output[:, 1]
    
def run_UMAP_GPU(onehot_input, df=None, init="random", random_state=42, min_dist=0.01, n_neighbors=20, densmap=False, verbose=True):
    """An implement of UMAP (GPU version).
   
    Parameters
    ----------
    onehot_input: iterable.
        A list of one-hot encoded sequences.
    df: pd.DataFrame
        A DataFrame to process. If given, it will return a DataFrame with X and Y columns. If not, it will return X and Y, separatively.
    init: str.
        init value for UMAP.
    random_state: int
        random seed.
    min_dist: float
        min_dist for UMAP
    n_neighbors: int
        n_neighbors for UMAP
    densmap: boolean
        If use DensMAP.
    verbose: boolean
        verbose level

    Returns
    -------
    A DataFrame or [X and Y]
    """
    import cuml
   
    model = cuml.UMAP(init=init, random_state=random_state, n_components=2, min_dist=min_dist, n_neighbors=n_neighbors, verbose=verbose, densmap=densmap)
    umap_output = model.fit_transform(onehot_input)
    
    if df is not None:
        df = df.copy()
        df["X"] = umap_output[:, 0]
        df["Y"] = umap_output[:, 1]
        del model
        return df
    else:
        del model
        return umap_output[:, 0], umap_output[:, 1]

def get_sparse_matrix_from_indices_distances_umap(
        knn_indices, knn_dists, n_obs, n_neighbors
    ):
    """A helper function for Louvain and Leiden. Adopted from Scanpy.
   
    Parameters
    ----------
    knn_indices: object
    knn_dists: object
    n_obs: int
    n_neighbors: int
    """
    import numpy as np
    from scipy.sparse import issparse, coo_matrix, csr_matrix
    rows = np.zeros((n_obs * n_neighbors), dtype=np.int64)
    cols = np.zeros((n_obs * n_neighbors), dtype=np.int64)
    vals = np.zeros((n_obs * n_neighbors), dtype=np.float64)

    for i in range(knn_indices.shape[0]):
        for j in range(n_neighbors):
            if knn_indices[i, j] == -1:
                continue  # We didn't get the full knn for i
            if knn_indices[i, j] == i:
                val = 0.0
            else:
                val = knn_dists[i, j]

            rows[i * n_neighbors + j] = i
            cols[i * n_neighbors + j] = knn_indices[i, j]
            vals[i * n_neighbors + j] = val

    result = coo_matrix((vals, (rows, cols)), shape=(n_obs, n_obs))
    result.eliminate_zeros()
    return result.tocsr()

def compute_connectivities_umap(
        knn_indices,
        knn_dists,
        n_obs,
        n_neighbors,
        set_op_mix_ratio=1.0,
        local_connectivity=1.0,
    ):
    """A helper function for Louvain and Leiden. Adopted from Scanpy.
   
    Parameters
    ----------
    knn_indices: object
    knn_dists: object
    n_obs: int
    n_neighbors: int
    set_op_mix_ratio: float
    local_connectivity: float
    """
    from scipy.sparse import issparse, coo_matrix, csr_matrix
    from umap.umap_ import fuzzy_simplicial_set
    X = coo_matrix(([], ([], [])), shape=(n_obs, 1))
    connectivities = fuzzy_simplicial_set(
        X,
        n_neighbors,
        None,
        None,
        knn_indices=knn_indices,
        knn_dists=knn_dists,
        set_op_mix_ratio=set_op_mix_ratio,
        local_connectivity=local_connectivity,
    )

    if isinstance(connectivities, tuple):
        # In umap-learn 0.4, this returns (result, sigmas, rhos)
        connectivities = connectivities[0]

    distances = get_sparse_matrix_from_indices_distances_umap(
        knn_indices, knn_dists, n_obs, n_neighbors
    )

    return distances, connectivities.tocsr()

def get_igraph_from_adjacency(adjacency, directed=None):
    """A helper function for Louvain and Leiden. Adopted from Scanpy.
   
    Parameters
    ----------
    adjacency: object
        Generated by compute_connectivities_umap
    
    Returns
    -------
    iGraph object
    """
    import numpy as np
    import igraph as ig
    sources, targets = adjacency.nonzero()
    weights = adjacency[sources, targets]
    if isinstance(weights, np.matrix):
        weights = weights.A1
    g = ig.Graph(directed=directed)
    g.add_vertices(adjacency.shape[0])  # this adds adjacency.shape[0] vertices
    g.add_edges(list(zip(sources, targets)))
    try:
        g.es['weight'] = weights
    except KeyError:
        pass
    return g

def get_igraph(onehot_input, random_state=42, metric="euclidean", n_neighbors=20, metric_kwds={}, n_jobs=6, angular=False, verbose=False):
    """Prepare iGraph object for Louvain and Leiden
   
    Parameters
    ----------
    onehot_input: np.array
        The one-hot encoded sequences.
    random_state: int
        Random seed.
    metric: str
        Same as UMAP performed.
    n_neighbors: int
        Same as UMAP.
    metric_kwds: dict
    angular: boolean
    verbose: boolean
    
    Returns
    -------
    iGraph object
    """

    from umap.umap_ import nearest_neighbors

    n_obs = onehot_input.shape[0]
    
    knn_indices, knn_dists, forest = nearest_neighbors(
            onehot_input,
            n_neighbors,
            random_state=random_state,
            metric=metric,
            metric_kwds=metric_kwds,
            angular=angular,
            verbose=verbose,
            n_jobs=n_jobs,
        )
      
    distances, connectivities = compute_connectivities_umap(knn_indices, knn_dists, n_obs, n_neighbors, set_op_mix_ratio=1.0, local_connectivity=1.0)
 
    g = get_igraph_from_adjacency(connectivities)
    return g
    
if __name__ == "__main__":
    pass