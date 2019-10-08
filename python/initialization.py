import networkx as nx
import numpy as np
import pandas as pd
import math


def initialization(adjacency, propSample, m, n):
    layerSet = np.tile(math.ceil(propSample * n), np.random.choice(range(1, m), math.ceil(m/2)))
    neighborhoods = nx.neighbors(adjacency, 1)
    keepSample = np.random.choice(range(1, n), math.ceil(propSample * n))
    neighborhoods = neighborhoods[keepSample]
    return list(neighborhoods, layerSet)