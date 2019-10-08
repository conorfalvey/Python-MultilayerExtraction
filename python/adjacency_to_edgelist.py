import networkx as nx
import numpy as np
import pandas as pd


def adjacencyToEdgelist(adjacency, mode=['undirected', 'directed'], weighted=None):
    # Make input a list object
    if not isinstance(adjacency, list):
        adjacency = list(adjacency)

    matrix = np.asmatrix(adjacency)

    mode = mode[0]
    adjLen = len(adjacency)
    edgeList = [0, 0, 0]

    if mode == "undirected":
        directed = False
    else:
        directed = True

    for i in range(1, adjLen):
        # Convert adjacency matrix to NetworkX Object
        tempGraph = nx.convert.from_numpy_matrix(matrix[i], parallel_edges=False)

        # edge = get.edgeList(tempGraph)
        edge = nx.read_weighted_edgelist(tempGraph)
        # boundEdges = cbind(edge, i)
        boundEdges = pd.concat([edge, i], axis=1)
        # edgeList = rbind(edgeList, boundEdges)
        edgeList = pd.concat([edgeList, boundEdges], axis=1)

    edgeList = edgeList[-1:]
    # TODO: Column names
    edgeList.columns = ['node1', 'node2', 'node3']
    return edgeList