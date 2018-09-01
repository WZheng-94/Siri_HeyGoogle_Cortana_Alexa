# python cohash_network.py True ipfile opfile

import pandas as pd 
import networkx as nx 
import sys
import heapq

PATH = '../data/'

def make_graph(file, minf, top, english=True):
	'''
	df is the whole data file
	'''

	df = pd.read_csv(file)
	if english:
		hashtag = df[df['lang'] == 'en']['hashtags']
	else:
		hashtag = df.hashtags

	G = nx.Graph()

	hashtag = hashtag[~hashtag.isnull()]
	edges = {}
	nodes = {}
	for cell in hashtag:
		node_list = cell.split('; ')
		if len(node_list) > 1:


			for edge in edge_list:
				edges[edge] = edges.get(edge, 0) + 1
		else:
			node = node_list[0]
			nodes[node] = nodes.get(node, 0) + 1


	edge_list = [(*x, edges[x]) for x in edges.keys()]

	G.add_weighted_edges_from(edge_list)

	return G


def get_top_node(top, node_dic):

    node_counts = list(node_dic.items())

    h = [(count,n) for (n,count) in node_counts[:top]]
    heapq.heapify(h)

    for n, count in node_counts[top:]:
        min_count, min_n = h[0]

        if count > min_count:
            heapq.heapreplace(h, (count, n))

    h.sort(reverse=True)

    return h




if __name__ == '__main__':

	english, ipfile, opfile = sys.argv[1:]

	english = eval(english)
	ipfile = PATH + ipfile
	opfile = PATH + opfile

	G = make_graph(ipfile, english)

	nx.write_gexf(G, opfile)




	



