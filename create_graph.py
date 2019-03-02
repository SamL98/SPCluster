import networkx as nx

def create_graph():
	with open('data/similar_pairs.txt') as f:
		pairs = f.read().split('\n')[:-1]

	G = nx.Graph()

	existing_ids = []

	for row in pairs:
		pair = row.split(',')
		tid1, tid2 = pair[0], pair[1]

		if not tid1 in existing_ids:
			G.add_node(tid1)
			existing_ids.append(tid1)

		if not tid2 in existing_ids:
			G.add_node(tid2)
			existing_ids.append(tid2)

		G.add_edge(tid1, tid2)

	return G, existing_ids

def adj_matrix():
	g, ids = create_graph()
	return nx.to_scipy_sparse_matrix(g), ids
