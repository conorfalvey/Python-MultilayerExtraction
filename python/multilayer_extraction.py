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



    # detectCores detects the number of cores available on your instance

    '''
    registerDoParallel(detectCores())
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
    '''


'''
  #detectCores detects the number of cores available on your instance

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