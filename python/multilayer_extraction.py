import itertools as it
import math
import multiprocessing as mp
import networkx as nx
import numpy as np
import pandas as pd
import random
from . import adjacency_to_edgelist as adj_to_edge
from . import edgelist_to_degree_sequence as edge_to_deg
from . import expectation_CM as expCM
from . import format_edgelist
from . import initialization as init
from . import score


def multilayer_extraction(edgelist, seed, min_score, prop_sample):
    m = max(list(edgelist['layer']))
    n = len(np.unique(edgelist['node1'].append(edgelist['node2'])))

    # Calculate the Modularity Matrix
    # Use Expectation_CM
    print("Estimation Stage")
    mod_mat = expCM.expectation_CM(edgelist)

    # Initialize the Communities
    print("Initialization Stage")
    initial_set = None
    for i in range(0, m + 1):
        graph = nx.parse_edgelist(format_edgelist.format_edgelist(edgelist[edgelist['layer'] == i]))
        if i == 0:
            initial_set = init.initialization(graph, prop_sample, m, n)
        else:
            initial_set.append(init.initialization(graph, prop_sample, m, n))

    # Search Across Initial Sets
    print("Search Stage")

    print("Seaching over", len(initial_set['vertex_set']), "seed sets \n", sep=" ")
    results_temp = list()
    k = len(initial_set['vertex_set'])

    # Detect number of cores present on your machine
    cores = mp.cpu_count()
    for i in range(0, k):
        starter = pd.DataFrame()
        starter['vertex_set'] = initial_set["vertex_set"][i]
        if len(starter["vertex_set"] < 2):
            starter["vertex_set"] = np.r_(starter["vertex_set"], list(set(range(1, n)) - set(starter["vertex_set"]))[i])
        starter["layer_set"] = initial_set["layer_set"][i]
        temp = single_swap(starter, mod_mat, m, n)
        results_temp.extend(temp)


    print("Cleaning Stage")
    if len(results_temp) < 1:
        return "No Community Found"

    scores = np.repeat(0, len(results_temp))

    for i in range(1, len(results_temp)):
        if (len(results_temp["layer_set"][i]) == 0):
            scores[i] = -1000
        if (len(results_temp["layer_set"][i]) > 0):
            scores[i] = results_temp[i]

    scores = round(scores[5])
    indx = np.where()

    return None


'''

  Scores = round(Scores, 5)
  #keep only unique communities with score greater than threshold
  indx = which(!duplicated(Scores) == TRUE)
  indx.2 = which(Scores > min.score)
  Results2 = Results.temp[intersect(indx, indx.2)]
  if(length(Results2) == 0){
    Results = NULL
    return(Object = NULL)
  }
  if(length(Results2) > 0){
    betas = seq(0.01, 1, by = 0.01)
    Results3 = list()
    Number.Communities = rep(0, length(betas))
    Mean.Score = rep(0, length(betas))
    for(i in 1:length(betas)){
      temp = cleanup(Results2, betas[i])
      Results3[[i]] = list(Beta = betas[i], Communities = temp$Communities)
      Mean.Score[i] = temp$Mean.Score
      Number.Communities[i] = length(temp$Communities)
    }
  }
  
  Z = data.frame(Beta = betas, Mean.Score = Mean.Score, Number.Communities = Number.Communities)
  Object = list(Community.List = Results3, Diagnostics = Z)
  class(Object) = "MultilayerCommunity"
  return(Object)
'''

def single_swap(initial_set, mod_mat, m, n):
    B_new = initial_set['vertex_set']
    I_new = initial_set['layer_set']
    score_old = score.score(mod_mat, B_new, I_new, n)

    iterations = 1
    B_fixed = B_new + 1
    I_fixed = I_new + 1


    while(len([value for value in B_fixed if value in B_new]) < max(len(B_fixed), len(B_new))
          or len([value for value in I_fixed if value in I_new]) < max(len(I_fixed), len(I_new))):
        if len(B_new) < 2 or len(I_new) < 1:
            print('No community found')
            return None

        B_fixed = B_new
        I_fixed = I_new

        B = B_new
        I = I_new + 1

        if m > 1:
            while len([value for value in I_new if value in I]) < max(len(I_new), len(I)):
                I = I_new
                results = swap_layer(mod_mat, I, B, score_old, m, n)
                I_new = results['layer_set']
                score_old = results['score_old']
        if m == 1:
            I_new = 1

        B = B - 1
        B_new = B + 1

        while len([value for value in B_new if value in B]) < max(len(B_new), len(B)):
            B = B_new
            results = swap_vertex(mod_mat, I_new, B, score_old, m, n)

            B_new = results['B_new']
            score_old = results['score_old']

    return pd.DataFrame({'B': B_new.sort(), 'I': I_new.sort(), 'Score': score_old})


def swap_layer(mod_mat, layer_set, vertex_set, score_old, m, n):
    if len(layer_set) == 0:
        print('No Community Found')
        return None

    changes = layer_change(mod_mat, layer_set, vertex_set, score_old, m, n)
    changes = [0 for value in changes if math.isnan(value)]
    changes = [0 for value in changes if value is None]

    outside_candidate = np.where(changes[changes in list(set(range(0, m)).difference(set(layer_set)))])
    l_add = list(set(range(0, m)) - set(layer_set))[list in outside_candidate]

    inside_candidate = np.where(changes[layer_set])
    l_sub = layer_set[inside_candidate]

    results = swap_candidate(layer_set, changes, l_add, l_sub, score_old)
    layer_set_new = results['set_new']
    score_old = results['score_old']

    return pd.DataFrame({'layer_set_new': layer_set_new, 'score_old': score_old})


def layer_change(mod_mat, layer_set, vertex_set, score_old, m, n):
    indx = list(set(range(1, m)) - set(layer_set))
    score_changes = [0] * m

    for i in range(1, m + 1):
        if i in indx:
            score_changes[i] = score.score(mod_mat, vertex_set, set(layer_set).union(i), n) - score_old
        if not i in indx:
            score_changes[i] = score.score(mod_mat, vertex_set, list(set(layer_set) - set(i)), n) - score_old

    return score_changes


def swap_candidate(set, changes, add, remove, score_old):
    if len(remove) == 0 and len(add) > 0:
        if add is not None:
            if changes[add] > 0:
                set_new = set.union(add)
                score_old = score_old + changes[add]
            if changes[add] < 0:
                set_new = set
                return pd.DataFrame({'set_new': set_new, 'score_old': score_old})

    if len(add) == 0 and len(remove) > 0:
        if remove is not None:
            if changes[remove] > 0:
                set_new = set - remove
                score_old = score_old + changes[remove]
                return pd.DataFrame({'set_new': set_new, 'score_old': score_old})
            if changes[remove] < 0:
                set_new = set
                return pd.DataFrame({'set_new': set_new, 'score_old': score_old})

    if len(add) > 0 and len(remove) > 0:
        if changes[remove] < 0 and changes[add] < 0:
            set_new = set
            return pd.DataFrame({'set_new': set_new, 'score_old': score_old})
        if changes[remove] > changes[add] and changes[remove] > 0:
            set_new = set - remove
            score_old = score_old + changes[remove]
            return pd.DataFrame({'set_new': set_new, 'score_old': score_old})
        if changes[remove] < changes[add] and changes[add] > 0:
            set_new = set.union(add)
            score_old = score_old + changes[add]
            return pd.DataFrame({'set_new': set_new, 'score_old': score_old})

    if len(add) == 0 and len(remove) == 0:
        return pd.DataFrame({'set_new': set, 'score_old': score_old})


def swap_vertex(mod_mat, layer_set, vertex_set, score_old, m, n):
    if len(layer_set) == 0:
        print('No Community Found')
        return None

    if len(vertex_set) < 5 or len(vertex_set) == n:
        print('No Community Found')
        return None

    changes = vertex_change(mod_mat, layer_set, vertex_set, score_old, m, n)

    outside_candidate = np.where(changes[changes in list(set(range(1, m)) - set(vertex_set))])
    u_add = list(set(range(1, n)) - set(vertex_set))[list in outside_candidate]

    inside_candidate = np.where(changes[vertex_set])
    u_sub = vertex_set[inside_candidate]

    results = swap_candidate(vertex_set, changes, u_add, u_sub, score_old)
    return pd.DataFrame({'layer_set_new': results['set_new'], 'score_old': results['score_old']})


def vertex_change(mod_mat, layer_set, vertex_set, score_old, m, n):
    indx = list(set(range(1, n)) - set(vertex_set))
    score_changes = [0] * (n + 1)

    for i in range(1, n + 1):
        if i in indx:
            score_changes[i] = score.score(mod_mat, set(vertex_set).union(i), layer_set, n) - score_old
        else:
            score_changes[i] = score.score(mod_mat, list(set(vertex_set) - set(1)), layer_set, n) - score_old

    return score_changes
