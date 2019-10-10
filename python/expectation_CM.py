import networkx as nx
import numpy as np
import pandas as pd


def expectation_CM(adjacency):
    m = max(adjacency[:, 3])
    n = len(np.unique(np.r_(adjacency[:, 1], adjacency[:, 2])))

    P = list()
    for i in range(1, m):
        graph = nx.parse_edgelist(pd.DataFrame(adjacency)[i].values.tolist()[, 1:2])

        degrees = nx.degree(graph)
        degree_total = sum(degrees)
        expected = np.matmul(degrees, np.transpose(degrees)) / degree_total
        P[i] = nx.from_numpy_matrix(expected)

    return P
