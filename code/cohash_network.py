# python cohash_network.py minf top ipfile opfile
# purpose: create co-hashtag network, minf: minimum frequency
#          top: top nodes


import pandas as pd 
import networkx as nx 
import sys
import heapq
import itertools




def find_top_k(nodes, k):
	'''
	get a list of nodes with top frequency
	'''

	node_list = list(nodes.items())
	h = [(count,n) for (n,count) in node_list[:k]]
	heapq.heapify(h)

	for n, count in node_list[k:]:
		min_count, min_n = h[0]

		if count > min_count:
			heapq.heapreplace(h, (count, n))

	h.sort(reverse=True)
	rv = [n[1] for n in h]

	return rv


def find_min_f(nodes, f):
	'''
	get a list of nodes with least frequency
	'''

	rv = [node for node in nodes if nodes[node] >= f]

	return rv


def get_node_list(nodes, minf=0, top=None):


	if minf > 0:
		node_list = find_min_f(nodes, minf)
	elif top != None:
		node_list = find_top_k(nodes, top)
	else:
		node_list = list(nodes.keys())

	return node_list


def make_graph(file, minf=0, top=None):
	'''
	df is the whole data file
	'''

	df = pd.read_csv(file)
	hashtag = df[df['lang'] == 'en']['hashtags']
	hashtag = hashtag[~hashtag.isnull()]

	edges = {}
	nodes = {}

	for cell in hashtag:
		node_list = cell.split('; ')
		node_list = list(set([node.lower() for node in node_list]))
		for node in node_list:
			nodes[node] = nodes.get(node, 0) + 1


	# it's impossible that both minf > 0 and top != None
	node_list = get_node_list(nodes, minf, top)

	for cell in hashtag:
		nodes = cell.split('; ')
		nodes = list(set([node.lower() for node in nodes]))
		if len(nodes) > 1:
			for node in nodes:
				if not node in node_list:
					nodes.remove(node)
			edge_list = list(itertools.combinations(nodes, 2))
			for edge in edge_list:
		 		edges[edge] = edges.get(edge, 0) + 1


	edge_list = [pair for pair in edges if (pair[0] in node_list) and (pair[1] in node_list)]

	pairs = list(edges.keys())
	for pair in pairs:
		if not pair in edge_list:
			del edges[pair]

	edge_list = [(*x, edges[x]) for x in edges.keys()]
	G = nx.Graph()
	G.add_weighted_edges_from(edge_list)

	return G



def main():

	minf, top, ipfile, opfile = sys.argv[1:]
	G = make_graph(ipfile, int(minf), int(top))
	nx.write_gexf(G, opfile)


if __name__ == '__main__':

	main()




	



