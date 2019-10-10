import networkx as nx
# import numpy as np
import pandas as pd


def adjacencyToEdgelist(adjacency, mode='undirected', weighted=None):
    # Make input a list object
    if not isinstance(adjacency, list):
        adjacency = list(adjacency)

    # matrix = np.asmatrix(adjacency)

    # mode = mode[0]
    adj_len = len(adjacency)
    edge_list = [0, 0, 0]

    '''
    if mode == "undirected":
        directed = False
    else:
        directed = True
    '''

    for i in range(1, adj_len):
        # Convert adjacency matrix to NetworkX Object
        temp_graph = '''nx.convert.from_numpy_matrix(matrix[i], parallel_edges=False)'''

        # edge = get.edgeList(tempGraph)
        edge = nx.read_weighted_edgelist(temp_graph)
        # boundEdges = cbind(edge, i)
        bound_edges = pd.concat([edge, i], axis=1)
        # edgeList = rbind(edgeList, boundEdges)
        edge_list = pd.concat([edge_list, bound_edges], axis=1)

    edge_list = edge_list[-1:]
    # TODO: Column names
    edge_list.columns = ['node1', 'node2', 'node3']
    return edge_list
