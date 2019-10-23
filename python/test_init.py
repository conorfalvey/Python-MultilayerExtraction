# Testing Setup of Multilayer Extraction
import networkx as nx
import pandas as pd
import numpy as np
import math
import random
import matplotlib.pyplot as plt
import itertools as it

#Gen default testing graph
graph = nx.generators.complete_graph(9)
#Gen adjacency matrix for complete graph
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

#Gen edgelist from adjacency matrix
edgelist = pd.DataFrame({'node1': [0], 'node2': [0], 'layer': [0]})
m = len(adjacency)

for i in range(0, m):
    temp_graph = nx.from_numpy_matrix(np.asarray(adjacency[i]), False)
    edges = nx.convert_matrix.to_pandas_edgelist(temp_graph)
    edges = edges.drop(['weight'], axis=1)
    edges = edges.rename(columns={"source": "node1", "target": "node2"})
    edges['layer'] = i
    edgelist = edgelist.append(edges)

edgelist = edgelist.reset_index(drop=True)
edgelist = edgelist.drop(edgelist[edgelist['node1'] == edgelist['node2']].index)
edgelist = edgelist.reset_index(drop=True)

print(edgelist)

#Gen Expectation.CM from edgelist
m = max(edgelist['layer'])
p = list()
for i in range(0, m + 1):
    sub = edgelist[edgelist['layer'] == i][['node1', 'node2']]
    lines = list()
    for _, row in sub.iterrows():
        lines.append(" ".join([str(row['node1']), str(row['node2'])]))
    graph = nx.parse_edgelist(lines)
    degrees = np.array(list(dict(graph.degree()).values()))
    degree_total = degrees.sum()
    expected = np.dot(degrees.reshape(degrees.size, 1), degrees.reshape(1, degrees.size))/degree_total
    p.append(nx.from_numpy_matrix(np.asarray(expected), False))

nx.draw(p[0])
#plt.show()

#Gen initialization outputs
m = 1
n = 9
prop_sample = 0.05

layer_set = list()
for i in range(0, math.ceil(prop_sample * n)):
    layer_set.append(random.sample(range(0, m), math.ceil(m/2)))
neighborhoods = list()
for i in graph.nodes():
    neighborhoods.append(list([i]) + list(graph.neighbors(i)))
keep_sample = random.sample(range(1, n), math.ceil(prop_sample * n))
neighborhoods = [neighborhoods[i] for i in keep_sample]
initial = pd.DataFrame({'vertex_set': neighborhoods, 'layer_set': layer_set})

print(initial)

#Gen score
n = 9
vertex_set = initial['vertex_set']
layer_set = initial['layer_set']
adjacency_score = p
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

