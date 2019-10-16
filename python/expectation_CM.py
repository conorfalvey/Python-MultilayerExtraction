# expectation_CM
#
# Function that calculates the expected edge weight between each pair of nodes in each layer of a multilayer network
# @param edgelist: a matrix with three columns representing edge connections: node1, node2, layer
# @future_param directed: directed or undirected
#
# @keywords community detection, multilayer networks, configuration model, random graph models
# @return list of NetworkX Graphs of the expected edge weights
#
# Basis: Wilson, James D., Palowitch, John, Bhamidi, Shankar, and Nobel, Andrew B. (2017) "Significance based
#        extraction in multilayer networks with heterogeneous community structure." Journal of Machine Learning Research
# Original R Code: James D. Wilson
# Revised Python Code: Conor Falvey
import networkx as nx
import numpy as np


def expectation_CM(edgelist):
    # Find highest layer to loop over. Also functions to confirm data is structured coming in.
    m = max(edgelist['layer'])

    # p: an empty list to contain graph objects appended each loop
    p = list()
    for i in range(0, m):
        # Sub contains the two node columns from the edgelist for a given layer i
        sub = edgelist[edgelist['layer'] == i][['node1', 'node2']]

        # NetworkX.parse_edgelist() works on a list of strings of format "x y". Here we preprocess for that call
        lines = list()
        # Iterate over the rows of the sub and join the two values of the nodes together with a " " delimiter
        for _, row in sub.iterrows():
            lines.append(" ".join([str(row['node1']), str(row['node2'])]))
        # Finally, call NetworkX.parse_edgelist on the list of formatted node string pairs
        graph = nx.parse_edgelist(lines)

        # Graph.degree() is an array-like object but has no value extraction method, so we wrap it as a dictionary and
        # extract the values from there, then convert to a list so we can wrap it finally in a NumPy Array.
        degrees = np.array(list(dict(graph.degree()).values()))
        degree_total = degrees.sum()
        # NumPy.dot() returns a scalar is we don't shape the vectors beforehand. By reshaping the two vectors with
        # dimensions n x m and m x n, the resultant matrix is of dimension n x n
        expected = np.dot(degrees.reshape(3, 1), degrees.reshape(1, 3))/degree_total

        # Append the resulting NetworkX graph object to the list P
        p.append(nx.from_numpy_matrix(np.asarray(expected), False))

    return p
