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


def score(adjacency, vertex_set, layer_set, n):
    return None


'''
score = function(mod.matrix, vertex.set, layer.set, n){
  
  if(length(layer.set) < 1 || length(vertex.set) < 1){
    return(obs.score = 0)
  }
  
  if(length(layer.set) == 1){
    super.mod <- mod.matrix[[layer.set]] #just a single igraph object
  }
  
  if(length(layer.set) > 1){
    #merge the modularity graphs
    super.mod <- graph.empty(n = n, directed = FALSE)
    for(j in layer.set){
      super.mod <- igraph::union(super.mod, mod.matrix[[j]]) #take union of all networks in the layer.set
    }
  }
    #take sub-graph of the modularity matrix
    super.mod.subgraph <- induced_subgraph(super.mod, v = vertex.set)
    
    #get the edge weights all together
    edge.weights <- as.data.frame(get.edge.attribute(super.mod.subgraph))
    edge.weights[is.na(edge.weights)] <- 0
    modularity.score <- rowSums(edge.weights) #sum across vertices first
    modularity.score[which(modularity.score < 0)] <- 0 #only keep positive values
    
    tot.mod <- sum(modularity.score)
    obs.score <- (tot.mod)^2 / (n^2*choose(length(vertex.set), 2)*(length(layer.set)))
    
    return(obs.score)
  }
'''