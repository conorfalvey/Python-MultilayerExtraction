# format_edgelsit
#
# Auxiliary function that converts an edgelist into a formatted edgelist to be passed to nx.parse_edgelist()
# @param edgelist: edgelist of node connections per layer
#
# keywords: community detection, multilayer networks, configuration model, random graph models
# @return: a list of vertex-set and layer combinations of statistically significance
#
# Basis: Wilson, James D., Palowitch, John, Bhamidi, Shankar, and Nobel, Andrew B. (2017) "Significance based
#        extraction in multilayer networks with heterogeneous community structure." Journal of Machine Learning Research
# Original R Code: James D. Wilson
# Revised Python Code: Conor Falvey
import numpy as np


def format_edgelist(edgelist):
    lines = list()
    # Iterate over the rows of the sub and join the two values of the nodes together with a " " delimiter
    for _, row in edgelist.iterrows():
        lines.append(" ".join([str(row['node1']), str(row['node2'])]))
    return lines
