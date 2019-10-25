# edgelist_to_degree_sequence
#
# Auxiliary function that converts an edgelist into a list of degree sequences by layer
# @param edgelist: edgelist of node connections per layer
# @param layer: Specific layer to return the degree sequence for that layer
#
# keywords: community detection, multilayer networks, configuration model, random graph models
# @return: a list of vertex-set and layer combinations of statistically significance
#
# Basis: Wilson, James D., Palowitch, John, Bhamidi, Shankar, and Nobel, Andrew B. (2017) "Significance based
#        extraction in multilayer networks with heterogeneous community structure." Journal of Machine Learning Research
# Original R Code: James D. Wilson
# Revised Python Code: Conor Falvey

import pandas as pd
from collections import Counter


# Return degree sequence for specific layer
def layer_degree_sequence(edgelist, layer):
    # Subset edgelist for given layer
    layer_set = edgelist[edgelist['layer'] == layer]
    # Stack columns of nodes and convert to a list
    tot_nodes = layer_set['node1'].append(layer_set['node2']).values.tolist()
    # Create a dataframe of nodes and degrees for those nodes with Python's Counter.keys() and Counter.values()
    degree = pd.DataFrame({'node': list(Counter(tot_nodes).keys()), 'degree': list(Counter(tot_nodes).values())})

    return degree


# Return list of degree sequences
def degree_sequence(edgelist):
    degrees = list()
    # Loop over every layer and append a call to layer_degree_sequence to the list above to return
    for i in range(0, len(edgelist['layer'] + 1)):
        degrees.append(layer_degree_sequence(edgelist, i))
    return degrees
