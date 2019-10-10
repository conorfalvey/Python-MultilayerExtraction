import networkx as nx
import pandas as pd
import math
import random

def initialization(adjacency, prop_sample, m, n):
    layer_set = list()
    for i in range(1, math.ceil(prop_sample * n)):
        layer_set[i] = random.sample(range(1, m), math.ceil(m/2))

    graph = nx.parse_edgelist(pd.DataFrame(adjacency)[i].values.tolist()[, 1:2])
    neighborhoods = list()
    for n in graph.nodes_iter:
        neighborhoods.append(nx.neighbors(graph, n))

    keep_sample = random.sample(range(1, n), math.ceil(prop_sample * n))
    neighborhoods = neighborhoods[keep_sample]

    return list(vertex_set = neighborhoods, layer_set = layer_set)
