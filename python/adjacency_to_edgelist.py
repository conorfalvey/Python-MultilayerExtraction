# adjacency_to_edgelist
#
# Function that converts a list of adjacency matrices to an edgelist
# @param adjacency: a list whose ith entry is an adjacency matrix representing the ith layer of a multilayer network
# @future_param mode: directed or undirected
# @future_param weighted: currently not functioning. Coming in later version.
#
# @keywords community detection, multilayer networks, configuration model, random graph models
# @return edgelist: a matrix with three columns representing edge connections: node1, node2, layer
#
# Basis: Wilson, James D., Palowitch, John, Bhamidi, Shankar, and Nobel, Andrew B. (2017) "Significance based
#        extraction in multilayer networks with heterogeneous community structure." Journal of Machine Learning Research
# Original R Code: James D. Wilson
# Revised Python Code: Conor Falvey
import networkx as nx
import numpy as np
import pandas as pd


def adjacency_to_edgelist(adjacency):
    # Instantiate labeled dataframe to make sure appends later on merge correctly
    edgelist = pd.DataFrame({'node1': [0], 'node2': [0], 'layer': [0]})
    m = len(adjacency)

    for i in range(0, m + 1):
        # Convert each matrix to a NetworkX Graph
        temp_graph = nx.from_numpy_matrix(np.asarray(adjacency[i]), False)

        # Convert NetworkX Graph to an edgelist and preprocess the resulting DataFrame
        edges = nx.convert_matrix.to_pandas_edgelist(temp_graph)
        edges = edges.drop(['weight'], axis=1)  # Drop unnecessary weight column (Unweighted graph)
        # Rename source and target columns to node1 and node2 (Undirected graph)
        edges = edges.rename(columns={"source": "node1", "target": "node2"})
        edges['layer'] = i  # Set a third column to the layer number
        edgelist = edgelist.append(edges)  # Now with correct data structures, we can append to the edgelist

    # The indices will be jumbled from many appends, so we can reset the index
    edgelist = edgelist.reset_index(drop=True)

    # Since we cannot selectively drop self looping edges in a NetworkX Graph structure,
    # we can do so here by creating a boolean series of entries who's nodes are equal,
    # and drop them from the DataFrame to preserve community structure later on.
    edgelist = edgelist.drop(edgelist[edgelist['node1'] == edgelist['node2']].index)
    # Since we dropped items in the line above, we must once again reset the indices
    edgelist = edgelist.reset_index(drop=True)

    return edgelist
