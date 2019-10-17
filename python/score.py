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
import networkx as nx
import numpy as np
import pandas as pd
import itertools as it
import math


def score(adjacency, vertex_set, layer_set, n):
    super_mod = None
    if len(layer_set) < 1 or len(vertex_set) < 1:
        return 0
    if len(layer_set) == 1:
        super_mod = adjacency[layer_set]
    if len(layer_set) > 1:
        super_mod = nx.empty_graph(n)
        for i in range(0, layer_set):
            super_mod = nx.union(super_mod, adjacency[i])

    super_mod_subgraph = super_mod.subgraph(vertex_set)

    edge_weights = pd.DataFrame(nx.get_edge_attributes(super_mod_subgraph, 'weight'))
    edge_weights = [0 for i in edge_weights if math.isnan(i)]
    modularity_score = np.sum(edge_weights, axis=1)
    modularity_score = [0 for i in modularity_score if i < 0]

    tot_mod = np.sum(modularity_score)
    obs_score = (tot_mod ** 2) / ((n ** 2 * it.combinations(range(0, len(vertex_set)), 2)) * (len(layer_set)))

    return obs_score
