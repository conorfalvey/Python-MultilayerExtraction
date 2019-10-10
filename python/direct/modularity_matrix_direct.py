import networkx as nx
import numpy as np
import pandas as pd


def multilayerModulatityMatrix(adjacency, directed = False):
    m = max(adjacency[:3])
    n = len(pd.unique(np.r_(adjacency[:1], adjacency[:2])))
    modMatrix = []

    for i in range(1, m):
        G = nx.parse_edgelist(pd.DataFrame(adjacency)[i].to_numpy()[, 1:2])
        G = nx.add_nodes(list(G.nodes)[n - len(list(G.nodes))])
        temp = nx.linalg.modularitymatrix(G)
        modMatrix[i] = nx.parse_adjlist(temp)

    return modMatrix