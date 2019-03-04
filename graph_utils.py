import pandas as pd
import numpy as np

def read_similair_pairs(fov):
	print('Reading similar pairs into DataFrame')
	similar_pairs = pd.read_csv('data/similar_pairs_fov%d.csv' % fov)

	tids = similar_pairs.loc[:,'tid1'].values
	tids = np.concatenate((tids, similar_pairs.loc[:,'tid2'].values))
	tids = np.unique(tids)

	return similar_pairs, tids

def create_transition_matrix(similar_pairs, num_tid):
	print('Creating the transition matrix')
	T = np.zeros((num_tid, num_tid), dtype=np.float64)
	tids = []

	for _, row in similar_pairs.iterrows():
		id1, id2 = row.tid1, row.tid2

		idx1 = len(tids)
		if id1 in tids: idx1 = tids.index(id1)
		else: 			tids.append(id1)

		idx2 = len(tids)
		if id2 in tids: idx2 = tids.index(id2)
		else: 			tids.append(id2)

		T[idx2, idx1] += row.weight

	return T