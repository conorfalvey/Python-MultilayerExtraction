import pandas as pd
from collections import Counter


def layer_degree_sequence(edgelist, layer):
    layer_set = edgelist[edgelist['layer'] == layer]
    tot_nodes = layer_set['node1'].append(layer_set['node2']).values.tolist()
    degree = pd.DataFrame({'node': list(Counter(tot_nodes).keys()), 'degree': list(Counter(tot_nodes).values())})

    return degree


def degree_sequence(edgelist):
    degrees = list()
    for i in range(0, len(edgelist['layer'] + 1)):
        degrees.append(layer_degree_sequence(edgelist, i))
    return degrees
