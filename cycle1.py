# import subprocess, sys
# subprocess.check_call([sys.executable, "-m", "pip", "install", "networkx>=3.4"], stdout=subprocess.DEVNULL)

import networkx as nx, numpy as np
import math

def random_weighted_digraph(num_nodes: int, edge_prob: float) -> nx.DiGraph:
    G = nx.gnp_random_graph(num_nodes, edge_prob, directed=True)
    for u, v in G.edges():
        G.edges[u,v]['weight'] = np.random.randint(1, 100)
    return G

def random_weighted_dgnm(num_nodes: int, edge_nodes: int) -> nx.DiGraph:
    G = nx.gnm_random_graph(num_nodes, edge_nodes, directed=True)
    for u, v in G.edges():
        G.edges[u,v]['weight'] = np.random.randint(1, 100)
    return G

def WeightedDiGraph(*edges: list[tuple[int,int,float]])->nx.DiGraph:
    """
    A shorthand function for quickly generating a directed graph with weights on the edges

    >>> G = WeightedDiGraph([0,1,55],[1,2,66],[2,0,77])
    >>> G.edges[0,1]
    {'weight': 55}
    """
    return nx.DiGraph( [(u,v,{"weight":w}) for u,v,w in edges])
    

def has_cycle1(graph: nx.DiGraph)->bool:
    """
    return True iff the given graph has a directed cycle in which the product of weights is smaller than 1.

    >>> has_cycle1(WeightedDiGraph())    # empty graph
    False
    >>> has_cycle1(WeightedDiGraph([0,1,55],[1,2,66],[2,0,77]))
    False
    >>> has_cycle1(WeightedDiGraph([0,1,0.55],[1,2,0.66],[2,0,0.77]))
    True
    """
    try:
        return nx.negative_edge_cycle(graph, weight=lambda u, v, d: math.log(d.get('weight', 1)))
    except ValueError:
        raise ValueError("Weights of graph must be positive in this func.")


def non_efficient_has_cycle1(graph: nx.DiGraph)->bool:
	"""
	A non-efficient implementation of has_cycle1, which is used for testing the correctness of the efficient one.

	>>> non_efficient_has_cycle1(WeightedDiGraph())    # empty graph
	False
	>>> non_efficient_has_cycle1(WeightedDiGraph([0,1,55],[1,2,66],[2,0,77]))
	False
	>>> non_efficient_has_cycle1(WeightedDiGraph([0,1,0.55],[1,2,0.66],[2,0,0.77]))
	True
	"""
	for cycle in nx.simple_cycles(graph):
		product = 1
		for i in range(len(cycle)):
			u = cycle[i]
			v = cycle[(i+1)%len(cycle)]
			product *= graph.edges[u,v].get('weight', 1)
		if product < 1:
			return True
	return False

if __name__ == '__main__':
    # edges = eval(input())
    # graph = WeightedDiGraph(*edges)
    # print(has_cycle1(graph))
    import doctest
    print (doctest.testmod())
