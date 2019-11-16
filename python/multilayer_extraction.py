import math
import multiprocessing as mp
import networkx as nx
import numpy as np
import pandas as pd
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
    results_temp = pd.DataFrame()
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
        if len(results_temp["layer_set"][i]) == 0:
            scores[i] = -1000
        if len(results_temp["layer_set"][i]) > 0:
            scores[i] = results_temp[i]

    scores = round(scores[5])
    indx = np.where(np.unique(scores))
    indx2 = np.where(scores > min_score)
    results2 = results_temp[list(set(indx).intersection(indx2))]

    betas = list()
    mean_score = list()
    number_communities = list()
    results3 = list()
    if len(results2) <= 0:
        results = None
        return None
    elif len(results2) > 0:
        betas = [1] * 100
        number_communities = [0] * len(betas)
        mean_score = [0] * len(betas)
        for i in range(0, len(betas)):
            temp = None  # Cleanup
            results3[i] = None  # List of betas and communities
            mean_score[i] = None  # mean score of temp list
            number_communities[i] = None  # length of temp communities

    z = pd.DataFrame({"Betas": betas, "Mean Score": mean_score, "Number Communities": number_communities})
    multi = pd.DataFrame({"Community List": results3, "Diagnostics": z})

    return multi


def single_swap(initial_set, mod_mat, m, n):
    b_new = initial_set['vertex_set']
    i_new = initial_set['layer_set']
    score_old = score.score(mod_mat, b_new, i_new, n)

    iterations = 1
    b_fixed = b_new + 1
    i_fixed = i_new + 1

    while (len([value for value in b_fixed if value in b_new]) < max(len(b_fixed), len(b_new))
           or len([value for value in i_fixed if value in i_new]) < max(len(i_fixed), len(i_new))):
        if len(b_new) < 2 or len(i_new) < 1:
            print('No community found')
            return None

        b_fixed = b_new
        i_fixed = i_new

        b = b_new
        i = i_new + 1

        if m > 1:
            while len([value for value in i_new if value in i]) < max(len(i_new), len(i)):
                i = i_new
                results = swap_layer(mod_mat, i, b, score_old, m, n)
                i_new = results['layer_set']
                score_old = results['score_old']
        if m == 1:
            i_new = 1

        b = b - 1
        b_new = b + 1

        while len([value for value in b_new if value in b]) < max(len(b_new), len(b)):
            b = b_new
            results = swap_vertex(mod_mat, i_new, b, score_old, m, n)

            b_new = results['B_new']
            score_old = results['score_old']

    return pd.DataFrame({'B': b_new.sort(), 'I': i_new.sort(), 'Score': score_old})


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
            score_changes[i] = score.score(mod_mat, vertex_set, set(layer_set).union({i}), n) - score_old
        if i not in indx:
            score_changes[i] = score.score(mod_mat, vertex_set, list(set(layer_set) - {i}), n) - score_old

    return score_changes


def swap_candidate(data_set, changes, add, remove, score_old):
    if len(remove) == 0 and len(add) > 0:
        if add is not None:
            if changes[add] > 0:
                set_new = data_set.union(add)
                score_old = score_old + changes[add]
            if changes[add] < 0:
                set_new = data_set
                return pd.DataFrame({'set_new': set_new, 'score_old': score_old})

    if len(add) == 0 and len(remove) > 0:
        if remove is not None:
            if changes[remove] > 0:
                set_new = data_set - remove
                score_old = score_old + changes[remove]
                return pd.DataFrame({'set_new': set_new, 'score_old': score_old})
            if changes[remove] < 0:
                set_new = data_set
                return pd.DataFrame({'set_new': set_new, 'score_old': score_old})

    if len(add) > 0 and len(remove) > 0:
        if changes[remove] < 0 and changes[add] < 0:
            set_new = data_set
            return pd.DataFrame({'set_new': set_new, 'score_old': score_old})
        if changes[remove] > changes[add] and changes[remove] > 0:
            set_new = data_set - remove
            score_old = score_old + changes[remove]
            return pd.DataFrame({'set_new': set_new, 'score_old': score_old})
        if changes[remove] < changes[add] and changes[add] > 0:
            set_new = data_set.union(add)
            score_old = score_old + changes[add]
            return pd.DataFrame({'set_new': set_new, 'score_old': score_old})

    if len(add) == 0 and len(remove) == 0:
        return pd.DataFrame({'set_new': data_set, 'score_old': score_old})


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
            score_changes[i] = score.score(mod_mat, set(vertex_set).union([i]), layer_set, n) - score_old
        else:
            score_changes[i] = score.score(mod_mat, list(set(vertex_set) - {1}), layer_set, n) - score_old

    return score_changes
