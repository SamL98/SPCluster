import numpy as np
import pandas as pd
import sys

from os.path import isfile
from sputil import fetch_library, get_track, read_spcsv

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

def perform_MCL(T, e=2, p=2, max_iter=100):	
	print('Performing MCL on the similarity graph')
	# Add the self loops to help MCL
	num_tid = len(T)
	T[np.arange(num_tid), np.arange(num_tid)] = 1

	# Normalize the columns of T
	T = T / T.sum(0)

	last_T = np.zeros_like(T)
	iter_no = 0

	while not np.allclose(last_T, T) and iter_no < max_iter:
		last_T = T.copy()
		iter_no += 1

		# Perform the expansion
		for _ in range(e-1):
			T = T.dot(T)

		# Perform the inflation
		for _ in range(p-1):
			T = T*T
			T = T / T.sum(0)
	
	print('MCL finished after %d iterations' % iter_no)
	return T

def parse_clusters(T):
	print('Parsing the clusters from MCL')
	clusters = []

	for i in range(len(T)):
		row = T[i]
		row[i] = 0

		if (row > 0).sum() > 0:
			attracted_mask = np.argwhere(row > 0).ravel()
			cluster = np.concatenate(([i], attracted_mask))
			clusters.append(cluster)
			T[attracted_mask,:] = 0

	print(f'{len(clusters)} clusters found')
	return np.array(clusters)

def disp_clusters(clusters, tids, fov):
	cluster_fname = 'clusters-fov%d.txt' % fov
	print(f'Writing the clusters to {cluster_fname}')

	f = open(cluster_fname, 'w')
	library = fetch_library()

	misc_track_fname = 'other_tracks.csv'
	other_tracks = pd.DataFrame(columns=library.columns)

	if isfile(misc_track_fname):
		other_tracks = read_spcsv(misc_track_fname)

	init_num_other_tracks = len(other_tracks)

	for cluster in clusters:
		if len(cluster) < 3: continue

		for idx in cluster:
			tid = tids[idx]
			rows = library.loc[lambda t: t.id == tid]

			if len(rows) == 0:
				rows = other_tracks.loc[lambda t: t.id == tid]

				if len(rows) == 0:
					track = get_track(tid)
					if track is None: continue

					title, artist = track['title'], track['artist']
					other_tracks.append(track, ignore_index=True)
				else:
					row = rows.iloc[0,:]
					title, artist = row.title, row.artist
			else:
				row = rows.iloc[0,:]
				title, artist = row.title, row.artist

			f.write(f'{title} -- {artist}\n')
		f.write('\n' + '*'*5 + '\n\n')
	f.close()

	if len(other_tracks) > init_num_other_tracks:
		other_tracks.to_csv(misc_track_fname)

if __name__ == '__main__':
	fov = 1
	if len(sys.argv) > 1:
		fov = int(sys.argv[1])

	similar_pairs, tids = read_similair_pairs(fov)
	T = create_transition_matrix(similar_pairs, len(tids))
	T = perform_MCL(T)
	clusters = parse_clusters(T)
	disp_clusters(clusters, tids, fov)