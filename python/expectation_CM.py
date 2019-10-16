# expectation_CM
#
# Function that calculates the extected edge weight between each pair of nodes in each layer of a multilayer network
# @param edgelist: a matrix with three columns representing edge connections: node1, node2, layer
# @future_param directed: directed or undirected
#
# @keywords community detection, multilayer networks, configuration model, random graph models
# @return ???
#
# Basis: Wilson, James D., Palowitch, John, Bhamidi, Shankar, and Nobel, Andrew B. (2017) "Significance based
#        extraction in multilayer networks with heterogeneous community structure." Journal of Machine Learning Research
# Original R Code: James D. Wilson
# Revised Python Code: Conor Falvey
import networkx as nx
import numpy as np
import pandas as pd


def expectation_CM(edgelist):
    m = max(edgelist['layer'])
    n = len(np.unique(edgelist['node1'].append(edgelist['node2'])))

    P = list()
    for i in range(0, m):
        sub = edgelist[edgelist['layer'] == i][['node1', 'node2']]
        lines = list()
        for index, row in sub.iterrows():
            lines.append(" ".join([str(row['node1']), str(row['node2'])]))
        graph = nx.parse_edgelist(lines)

        degrees = None





'''import networkx as nx
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
'''