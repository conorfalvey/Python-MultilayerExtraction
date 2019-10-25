# ***UNTESTED UNTESTED UNTESTED***
# score
#
# Function that calculates the score of a multilayer vertex - layer community
# @param expected(maybe adjacency?):
# @param vertex_set: Nodes within the multilayer community of interest
# @param layer_set: Layers within the multilayer community of interest
# @param n: Number of nodes per layer
#
# keywords: community detection, multilayer networks, configuration model, random graph models
# @return: a list of vertex-set and layer combinations of statistically significance
#
# Basis: Wilson, James D., Palowitch, John, Bhamidi, Shankar, and Nobel, Andrew B. (2017) "Significance based
#        extraction in multilayer networks with heterogeneous community structure." Journal of Machine Learning Research
# Original R Code: James D. Wilson
# Revised Python Code: Conor Falvey
import numpy as np
import pandas as pd
import itertools as it
import math
from . import edgelist_to_degree_sequence


def edge(edgelist, node1, node2, layer):
    for _, row in edgelist.iterrows():
        if row['layer'] == layer:
            if row['node1'] == node1:
                if row['node2'] == node2:
                    return 1
    return 0


def Q_calc(edgelist, degrees, vertex_set, l, n):
    tot_comb = 1 / (n * math.sqrt(len(list(it.combinations(range(0, len(vertex_set)), 2)))))

    summation = 0
    for i in range(0, len(vertex_set) + 1, -1):
        for j in range(0, i + 1, -1):
            temp = edge(edgelist, i, j, l)
            temp2 = degrees[degrees['node'] == i] * degrees[degrees['node'] == j]
            temp3 = temp2 / len(edgelist['node1'])
            temp4 = temp - temp3
            summation += temp4
    return tot_comb * summation


def score(edgelist, vertex_set, layer_set, n):
    layers = 1 / len(layer_set)
    degrees = edgelist_to_degree_sequence.degree_sequence(edgelist)
    summation = 0
    for i in range(0, layer_set + 1):
        summation += Q_calc(edgelist, degrees[i], vertex_set, i, n)

    return layers * summation ** 2


'''
def score(adjacency, vertex_set, layer_set, n):
    super_mod = None
    if len(layer_set) < 1 or len(vertex_set) < 1:
        print(0)
    if len(layer_set) == 1:
        super_mod = adjacency[layer_set[0][0]]
    if len(layer_set) > 1:
        super_mod = nx.empty_graph(n)
        for i in range(0, layer_set):
            super_mod = nx.union(super_mod, adjacency[i])

    super_mod_subgraph = super_mod.subgraph(map(int, vertex_set[0]))

    edge_weight_tuples = nx.get_edge_attributes(super_mod_subgraph, 'weight')
    edge_weights = pd.DataFrame({'edge': list(edge_weight_tuples.keys()), 'weight': list(edge_weight_tuples.values())})
    for _, weights in edge_weights.iterrows():
        if math.isnan(weights['weight']):
            weights['weight'] = 0

    modularity_score = np.sum(edge_weights['weight'])
    modularity_score = [0 for i in modularity_score if i < 0]

    tot_mod = np.sum(modularity_score)
    obs_score = (tot_mod ** 2) / ((n ** 2 * it.combinations(range(0, len(vertex_set)), 2)) * (len(layer_set)))

    print(obs_score)
'''
