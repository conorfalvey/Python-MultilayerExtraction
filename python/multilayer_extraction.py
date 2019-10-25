import itertools as it
import math
import multiprocessing
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
import matplotlib.pyplot as plt


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
    cores = multiprocessing.cpu_count()


    return "Fuck my life. Holy shit this is one big file. This makes me rethink my entire career."


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

    outside_candidate = np.where(changes[list(set(range(0, m)).difference(set(layer_set)))])
    l_add = list(set(range(0, m)) - set(layer_set))[outside_candidate]

    inside_candidate = np.where(changes[layer_set])
    l_sub = layer_set[inside_candidate]

    results = swap_candidate(mod_mat, layer_set, vertex_set, score_old, m, n)
    layer_set_new = results['set_new']
    score_old = results['score_old']

    return pd.DataFrame({'layer_set_new': layer_set_new, 'score_old': score_old})
'''
######Choosing which layer to swap one at a time######
swap.layer = function(adjacency, mod.matrix, layer.set, vertex.set, score.old, m, n){



  #Make the swap
  results <- swap.candidate(layer.set, changes, l.add, l.sub, score.old)
  layer.set.new <- results$set.new
  score.old <- results$score.old

  return(list(layer.set.new = layer.set.new, score.old = score.old))
}
'''















'''
multilayer.extraction = function(adjacency, seed = 123, min.score = 0, prop.sample = 0.05, directed = c(FALSE, TRUE)){

  registerDoParallel(detectCores())
  Results.temp <- foreach(i=1:K,.packages="MultilayerExtraction") %dopar% {
    starter <- list()
    starter$vertex.set <- as.numeric(initial.set$vertex.set[[i]])
    #if the initial neighborhood is of length 1, add a random vertex
    if(length(starter$vertex.set) < 2){
      starter$vertex.set <- c(starter$vertex.set, setdiff(1:n, starter$vertex.set)[1])
    }
    starter$layer.set <- as.numeric(initial.set$layer.set[[i]])
    single.swap(starter, adjacency, mod.matrix, m, n)
  }

  #Cleanup the results: Keep the unique communities
  print(paste("Cleaning Stage"))

  if(length(Results.temp) < 1){return("No Community Found")}

  Scores = rep(0, length(Results.temp))

  for(i in 1:length(Results.temp)){
    if(length(Results.temp[[i]]$B) == 0){Scores[i] = -1000}
    if(length(Results.temp[[i]]$B) > 0){
      Scores[i] = Results.temp[[i]]$Score
    }
  }
  
    scores = round(scores, 5)
    # keep only unique communities with score greater than threshold
    indx = np.where((not duplicated(scores)) == True)
    indx_2 = np.where(scores > min.score)
    results2 = results_temp[intersect(indx, indx_2)]
    if (len(results2) == 0):
        results = None
        return None
    if (len(results2) > 0):
        betas = seq(0.01, 1, by = 0.01)
        results3 = list()
        number_Communities = np.repeat(0, len(betas))
        mean_Score = np.repeat(0, len(betas))
        for i in range(1, len(betas)):
            temp = cleanup(results2, betas[i])
            results3[[i]] = list(Beta=betas[i], Communities=temp[Communities])
            mean_Score[i] = temp[Mean.Score]
            number_Communities[i] = len(temp[Communities])

  Z = data.frame(Beta = betas, Mean.Score = Mean.Score, Number.Communities = Number.Communities)
  Object = list(Community.List = Results3, Diagnostics = Z)
  class(Object) = "MultilayerCommunity"
  return(Object)
}


#######################################################################
##Swapping functions##
####Function for determining which vertex/layer should be swapped
swap.candidate = function(set, changes, add, remove, score.old){
  #If there are only some to be added
  if(length(remove) == 0 & length(add) > 0){
    if(is.na(add) == FALSE){
      if(changes[add] > 0){
        set.new <- union(set, add)
        score.old <- score.old + changes[add]
      }
      if(changes[add] < 0){
        set.new <- set
        return(list(set.new = set.new, score.old = score.old))
      }
    }
  }

  #If there are only some to removed
  if(length(add) == 0 & length(remove) > 0){
    if(is.na(remove) == FALSE){
      if(changes[remove] > 0){
        set.new <- setdiff(set,remove)
        score.old <- score.old + changes[remove]
        return(list(set.new = set.new, score.old = score.old))
      }
      if(changes[remove] < 0){
        set.new <- set
        return(list(set.new = set.new, score.old = score.old))
      }
    }
  }

  #If there are some to removed and some to be added
  if(length(add) > 0 & length(remove) > 0){
    if(changes[remove] < 0 & changes[add] < 0){
      set.new <- set
      return(list(set.new = set.new, score.old = score.old))
    }
    if(changes[remove] > changes[add] & changes[remove] > 0){
      set.new <- setdiff(set, remove)
      score.old <- score.old + changes[remove]
      return(list(set.new = set.new, score.old = score.old))
    }
    if(changes[remove] < changes[add] & changes[add] > 0){
      set.new <- union(set, add)
      score.old <- score.old + changes[add]
      return(list(set.new = set.new, score.old = score.old))
    }
  }

  #if there are none to be added nor removed
  if(length(add) == 0 & length(remove) == 0){
    return(list(set.new = set, score.old = score.old))
  }
}

######Choosing which layer to swap one at a time######
swap.layer = function(adjacency, mod.matrix, layer.set, vertex.set, score.old, m, n){

  if(length(layer.set) == 0){
    print('No Community Found')
    return(NULL)
  }

  changes <- layer.change(adjacency, mod.matrix, layer.set, vertex.set, score.old, m, n)
  changes[which(is.null(changes) == TRUE)] <- 0
  changes[which(is.na(changes) == TRUE)] <- 0

  outside.candidate <- which.max(changes[setdiff(1:m, layer.set)]) #which layer should we add?
  l.add <- setdiff(1:m, layer.set)[outside.candidate]

  inside.candidate <- which.max(changes[layer.set]) #which layer should we remove?
  l.sub <- layer.set[inside.candidate]

  #Make the swap
  results <- swap.candidate(layer.set, changes, l.add, l.sub, score.old)
  layer.set.new <- results$set.new
  score.old <- results$score.old

  return(list(layer.set.new = layer.set.new, score.old = score.old))
}

#######################################################################
######Choosing which vertex to swap one at a time######
swap.vertex = function(adjacency, mod.matrix, layer.set, vertex.set, score.old, m, n){

  if(length(layer.set) == 0){
    print('No Community Found')
    return(NULL)
  }

  #swap decision
  if(length(vertex.set) < 5){
    print('No Community Found')
    return(NULL)
  }

  if(length(vertex.set) == n){
    print('No Community Found')
    return(NULL)
  }
  changes = vertex.change(adjacency, mod.matrix, layer.set, vertex.set, score.old, m, n)

  #Get candidates
  outside.candidate <- which.max(changes[setdiff(1:n, vertex.set)])[1]
  u.add <- setdiff(1:n, vertex.set)[outside.candidate]

  inside.candidate <- which.max(changes[vertex.set])
  u.sub <- vertex.set[inside.candidate]

  #Make the swap
  results <- swap.candidate(vertex.set, changes, u.add, u.sub, score.old)
  return(list(B.new = results$set.new, score.old = results$score.old))
}
#######################################################################
#Inner function for a single swap inside the function for Multilayer.Extraction
#Note: check the names of initial set
single.swap = function(initial.set, adjacency, mod.matrix, m, n){

  #initialize vertex.set and layer.set
  B.new <- initial.set$vertex.set
  I.new <- initial.set$layer.set
  score.old <- score(mod.matrix, vertex.set = B.new, layer.set = I.new, n)

  iterations <- 1
  B.fixed <- B.new + 1
  I.fixed <- I.new + 1

  #main loop
  while(length(intersect(B.fixed, B.new)) < max(length(B.fixed), length(B.new)) |
        length(intersect(I.fixed, I.new)) < max(length(I.fixed), length(I.new))){

    if(length(B.new) < 2 | length(I.new) < 1){
      print('No community found')
      return(NULL)
    }

    #seems redundant, check...
    B.fixed <- B.new
    I.fixed <- I.new

    B <- B.new
    I <- I.new + 1

    #update layer set
    if(m > 1){
      while(length(intersect(I.new, I)) < max(length(I.new), length(I))){

        I <- I.new
        results <- swap.layer(adjacency, mod.matrix, I, B, score.old, m, n)
        I.new <- results$layer.set.new
        score.old <- results$score.old
      }
    }
    if(m == 1){
      I.new <- 1
    }

    #update vertex set
    B <- B - 1
    B.new <- B + 1

    while(length(intersect(B.new, B)) < max(length(B.new), length(B))){
      B <- B.new
      results <- swap.vertex(adjacency, mod.matrix, I.new, B, score.old, m, n)

      B.new <- results$B.new
      score.old <- results$score.old
    }
  }
  return(list(B = sort(B.new), I = sort(I.new), Score = score.old))
}

######Effect on score when adding or subtracting a layer#######
layer.change = function(adjacency, mod.matrix, layer.set, vertex.set, score.old, m, n){

  indx <- setdiff(1:m, layer.set) #which layers are not in the current set
  score.changes <- rep(0, m)

  for(i in 1:m){
    if(i %in% indx){
      score.changes[i] <- score(mod.matrix, vertex.set =
                                  vertex.set, layer.set = union(layer.set, i), n) - score.old
    }
    if(i %in% indx == FALSE){
      score.changes[i] <- score(mod.matrix, vertex.set =
                                  vertex.set, layer.set = setdiff(layer.set, i), n) - score.old
    }
  }
  return(score.changes)
}

######Effect on score when adding or subtracting a vertex#######
vertex.change = function(adjacency, mod.matrix, layer.set, vertex.set, score.old, m, n){

  indx <- setdiff(1:n, vertex.set)
  score.changes <- rep(0, n)

  #the following can also be parallelized!
  for(i in 1:n){
    if(i %in% indx){
      score.changes[i] <- score(mod.matrix, vertex.set =
                                  union(vertex.set, i), layer.set = layer.set, n) - score.old
    }
    if(i %in% indx == FALSE){
      score.changes[i] <- score(mod.matrix, vertex.set =
                                  setdiff(vertex.set, i), layer.set = layer.set, n) - score.old
    }
  }

  return(score.changes)
}

'''


'''
import networkx as nx
import numpy as np
import pandas as pd
import multiprocessing as mp
from expectation_CM import expectation_CM
from initialization import initialization


def multilayer_extraction(adjacency, seed, min_score, prop_sample, directed):
    # Adjacency should be an edgelist with three columns (node1, node2, layer)
    m = max(adjacency[:, 3])
    n = len(np.unique(np.r_(adjacency[:, 1], adjacency[:, 2])))
    directed = False
    print("Estimation Stage")

    mod_matrix = expectation_CM(adjacency)

    print("Initialization Stage")

    for i in range(1, m):
        if (i == 1):
            graph = nx.parse_edgelist(pd.DataFrame(adjacency)[i].values.tolist()[, 1:2])
            initial_set = initialization(graph, prop_sample, m, n)
        else:
            graph = nx.parse_edgelist(pd.DataFrame(adjacency)[i].values.tolist()[, 1:2])
            initial_set = np.r_(initial_set, initialization(graph, prop_sample, m, n))

    print("Search Stage")
    print("Searching over ", len(initial_set[1]), " seed sets")

    results_temp = list()
    k = len(initial_set[1])


    core_count = mp.cpu_count()
    results_temp = None


    Results.temp < - foreach(i=1: K, .packages = "MultilayerExtraction") % dopar % {
        starter < - list()
    starter$vertex.set < - as.numeric(initial.set$vertex.set[[i]])
    # if the initial neighborhood is of length 1, add a random vertex
    if (length(starter$vertex.set) < 2){
    starter$vertex.set < - c(starter$vertex.set, setdiff(1:n, starter$vertex.set)[1])
    }
    starter$layer.set < - as.numeric(initial.set$layer.set[[i]])
    single.swap(starter, adjacency, mod.matrix, m, n)
    }


    print("Cleaning Stage")
    if (len(results_temp) < 1):
        return("No Community Found")

    scores = np.repeat(0, len(results_temp))

    for i in range(1, len(results_temp)):
        if (len(results_temp[i][B]) == 0):
            scores[i] = -1000
        if (len(results_temp[i][B]) > 0):
            scores[i] = results_temp[i]

    # Z = pd.DataFrame(Beta=betas, Mean.Score = mean_score, Number_Communities = Number_communities)
    # Object = list(Community_list = result3, Diagnostics = Z)

    # class(Object) = "MultilayerCommunity"
    return None
'''