# initialization
#
# Function that identifies statistically significant vertex-layer communities in multilayer networks
# @param graph: Graph from edgelist used to find communities
# @param prop_sample: The proportion of vertices to search over for initialization
# @param m: number of layers
# @param n: number of nodes per layer
#
# keywords: community detection, multilayer networks, configuration model, random graph models
# @return: a list of vertex-set and layer combinations of statistically significance
#
# Basis: Wilson, James D., Palowitch, John, Bhamidi, Shankar, and Nobel, Andrew B. (2017) "Significance based
#        extraction in multilayer networks with heterogeneous community structure." Journal of Machine Learning Research
# Original R Code: James D. Wilson
# Revised Python Code: Conor Falvey
import networkx as nx
import pandas as pd
import math
import random


def initialization(graph, prop_sample, m, n):
    # Cannot find analog to R's replicate() function, so a wrapper for random sample appends is used
    layer_set = list()
    for i in range(0, math.ceil(prop_sample * n)):
        layer_set.append(random.sample(range(0, m), math.ceil(m/2)))
    # It doesn't appear that NetworkX has an analog for iGraph's neighborhood() function, so we iterate over the nodes
    # and append the neighbors of each node to the node itself to model the output of iGraph's neighborhoods() function
    neighborhoods = list()
    for i in graph.nodes():
        neighborhoods.append(list(i) + list(graph.neighbors(i)))
    # Generate random sample of indices for out sample to keep
    keep_sample = random.sample(range(1, n), math.ceil(prop_sample * n))
    # Subset neighborhoods with list comprehension for all values at keep_sample's indices
    neighborhoods = [neighborhoods[i] for i in keep_sample]
    # Return a DataFrame of the neighborhoods and the layer set to keep track of the vertex and layer sets
    return pd.DataFrame({'vertex_set': neighborhoods, 'layer_set': layer_set})
