# purpose: convert the two csv files of user network to .gexf
# command: python user_network.py user_node_csv user_edge_csv output

import pandas as pd 
import networkx as nx
import sys


def main():

	nodes, edges, opfile = sys.argv[1:]

	nodes_df = pd.read_csv(nodes)
	edges_df = pd.read_csv(edges)

	G = nx.DiGraph()

	for ind, row in nodes_df.iterrows():                    
		G.add_node(row['Label'], no_tweets = row['no_tweets'], no_mentions = row['no_mentions'])


	node_id_label = nodes_df.set_index('Id').Label.to_dict()

	for ind, row in edges_df.iterrows():
		source = node_id_label[row['Source']]
		target = node_id_label[row['Target']]
		G.add_edge(source,target,weight = row['Weight'])

	nx.write_gexf(G, opfile)

if __name__ == '__main__':
	main()
