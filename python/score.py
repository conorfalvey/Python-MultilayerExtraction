# ***UNTESTED UNTESTED UNTESTED***
# score
#
# Function that calculates the score of a multilayer vertex - layer community
# @param edgelist: edgelist of the expectation_CM
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


# Edge function takes in the edgelist, two nodes, and the layer of the nodes and returns a 0 or 1 depending on if those
# two nodes have a connecting edge in layer l.
def edge(edgelist, node1, node2, layer):
    # Iterate over rows in the edgelist
    for _, row in edgelist.iterrows():
        # Check if layer, node1, and node2 are all conditionally met
        if row['layer'] == layer and row['node1'] == node1 and row['node2'] == node2:
            return 1
    return 0


# Q_calc takes in an edgelist, vertex_set, layer, and nodes per layer and produces a score of the individual
# vertex-layer set.
def Q_calc(edgelist, degrees, vertex_set, layer, n):
    summation = 0
    # Iterate over i and j backwards as it's easier to define a relative bound working backwards.
    for i in range(0, len(vertex_set) + 1, -1):
        for j in range(0, i + 1, -1):
            # Calculate the proportion of the nodes from the degree sequence and divide by the length of the edgelist
            prop = (degrees[degrees['node'] == i] * degrees[degrees['node'] == j]) / len(edgelist['node1'])
            # Subtract this from the Identity function edge()
            summation += (edge(edgelist, i, j, layer) - prop)
    # Return the summation multiplied by the inverse of the total combinations of nodes possible.
    return 1 / (n * math.sqrt(len(list(it.combinations(range(0, len(vertex_set)), 2))))) * summation


# The score function finalizes the scoring by iterating over all the layers of the data, filtering for positive values,
# and return the summation squared times a scaling factor.
def score(edgelist, vertex_set, layer_set, n):
    # Convert the edgelist into a degree sequence to help performance
    degrees = edgelist_to_degree_sequence.degree_sequence(edgelist)
    summation = 0
    # Run Q_calc() on all layers and if the value is positive, add it to the summation
    for layer in range(0, layer_set + 1):
        q = Q_calc(edgelist, degrees[layer], vertex_set, layer, n)
        if q >= 0:
            summation += q
    # Return the resulting score multiplied by the scaling factor
    return 1 / len(layer_set) * summation ** 2
