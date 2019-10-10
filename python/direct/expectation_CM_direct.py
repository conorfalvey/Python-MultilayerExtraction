import networkx as nx
import numpy as np
import pandas as pd


def expectedCM(adjacency, directed = False):
    # check that adjacency is a list object
    # max of the layer index
    m = max(adjacency[:3])
    n = len(np.unique(np.r_(adjacency[:1], adjacency[:2])))

    p = []
    for i in range(1, m):
        G = nx.parse_edgelist(pd.DataFrame(adjacency)[i].to_numpy()[, 1:2])

        degrees = nx.degree(G)
        degTot = sum(degrees)
        expected = np.matrix_multiply(degrees, degrees.transpose())/degTot
        p[i] = nx.convert.from_numpy_matrix(expected, parallel_edges=False)

    return p

'''
        # Adjacency to dataframe
        # df = as.data.frame(adjacency)
        df = pd.DataFrame(adjacency)
        # Subset adjacency dataframe
        # sub = subset(df, layer == i)
        sub = df[i]
        # dataframe as matrix
        # mat = as.matrix(sub)
        mat = sub.to_numpy()
        # slice of matrix
        # slc = mat[, 1: 2]
        slc = mat[, 1:2]
        # graph from esgelist
        # G = graph_from_edgelist(slc, directed = directed)
        G = nx.parse_edgelist(slc)
'''