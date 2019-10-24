# Project Input/Output Formats

## Adjacency_to_edgelist
This can convert an list of adjacency matrices to a single edgelist. 
This is done for space preservation as instead of working with a list 
MxN sparse matrices, we have a three column list that contains all pertinent
information contained in the adjacency matrices.

### def adjacency_to_edgelist(adjacency):
This takes in a list of matrices:

![equation](https://latex.codecogs.com/gif.latex?m1%20%3D%20%5Cbegin%7Bbmatrix%7D%200%20%26%201%20%26%201%5C%5C%201%20%26%200%20%26%200%5C%5C%201%20%26%200%20%26%200%20%5Cend%7Bbmatrix%7D) &nbsp;&nbsp;
![equation](https://latex.codecogs.com/gif.latex?m2%20%3D%20%5Cbegin%7Bbmatrix%7D%201%20%26%201%20%26%201%5C%5C%201%20%26%200%20%26%201%5C%5C%201%20%26%201%20%26%200%20%5Cend%7Bbmatrix%7D) &nbsp;&nbsp;
![equation](https://latex.codecogs.com/gif.latex?m2%20%3D%20%5Cbegin%7Bbmatrix%7D%201%20%26%200%20%26%201%5C%5C%200%20%26%200%20%26%201%5C%5C%201%20%26%201%20%26%201%20%5Cend%7Bbmatrix%7D)

![equation](https://latex.codecogs.com/gif.latex?adjacency%20%3D%20%5Bm1%2C%20m2%2C%20m3%5D)

After running, this will output a [Pandas DataFrame](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html) with three
columns: node1, node2, and layer. It keeps track of unweighted, undirected 
edges between two nodes on the same layer and disregards self-loops. Our sample input above
would give the following edgelist:

![equation](https://latex.codecogs.com/gif.latex?edgelist%20%3D%20%5Cbegin%7Btabular%7D%7B%20%7Cc%7Cc%7Cc%7C%20%7D%20%5Chline%20Node1%20%26%20Node2%20%26%20Layer%20%5C%5C%20%5Chline%200%20%26%201%20%26%200%20%5C%5C%200%20%26%202%20%26%200%20%5C%5C%200%20%26%201%20%26%201%20%5C%5C%200%20%26%202%20%26%201%20%5C%5C%201%20%26%202%20%26%201%5C%5C%200%20%26%202%20%26%202%20%5C%5C%201%20%26%202%20%26%202%20%5C%5C%20%5Chline%20%5Cend%7Btabular%7D)

The initialization of the Pandas DataFrame is as follows:
```
edgelist = pd.DataFrame({'node1': [0], 'node2': [0], 'layer': [0]})
```

## Expectation_CM
This calculates the expected edge weight between each pair of 
nodes in each layer of a multilayer network. This takes in an edgelist and 
returns a list of NetworkX graphs representing the expected edge weights.

### def expectation_CM(edgelist):
This takes in an edgelist of the same format as the adjacency_to_edgelist output:
```
edgelist = pd.DataFrame({'node1': [0], 'node2': [0], 'layer': [0]})
```
