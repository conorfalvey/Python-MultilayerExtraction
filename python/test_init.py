# Testing Setup of Multilayer Extraction
import networkx as nx
import pandas as pd
import numpy as np
import math
import itertools as it
from . import adjacency_to_edgelist
from . import expectation_CM
from . import initialization
from . import score
import matplotlib.pyplot as plt

# Gen default testing graph
g1 = nx.planted_partition_graph(5, 25, 0.5, 0.05)
graph = nx.generators.complete_graph(9)
# Gen adjacency matrix for complete graph
adjacency = [[[0, 1, 1, 1, 1, 1, 1, 1, 1],
             [1, 0, 1, 1, 1, 1, 1, 1, 1],
             [1, 1, 0, 1, 1, 1, 1, 1, 1],
             [1, 1, 1, 0, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 0, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 0, 1, 1, 1],
             [1, 1, 1, 1, 1, 1, 0, 1, 1],
             [1, 1, 1, 1, 1, 1, 1, 0, 1],
             [1, 1, 1, 1, 1, 1, 1, 1, 0]]]
print(adjacency)

# Gen edgelist from adjacency matrix
edgelist = adjacency_to_edgelist.adjacency_to_edgelist(adjacency)

print(edgelist)

# Gen Expectation.CM from edgelist
expectation_CM = expectation_CM.expectation_CM(edgelist)

nx.draw(expectation_CM[0])
plt.show()

# Gen initialization outputs
initial = initialization.initialization(graph, 0.05, 1, 9)

print(initial)

# Gen score
# test_score = score.score(adjacency, initial['vertex_set'], initial['layer_set'], 9)

n = 9
vertex_set = initial['vertex_set']
layer_set = initial['layer_set']
adjacency_score = expectation_CM
super_mod = None
if len(layer_set) < 1 or len(vertex_set) < 1:
    print(0)
if len(layer_set) == 1:
    super_mod = adjacency_score[layer_set[0][0]]
if len(layer_set) > 1:
    super_mod = nx.empty_graph(n)
    for i in range(0, layer_set):
        super_mod = nx.union(super_mod, adjacency_score[i])

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

print(score.score(edgelist, vertex_set, layer_set, n))
