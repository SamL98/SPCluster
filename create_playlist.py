import numpy as np
import sys
from os.path import isfile

from sputil import read_spcsv, fetch_library, get_track
from graph_utils import *
from track_utils import *

def traverse_graph(T, seed_idx, tids, length=10):
	T[seed_idx,:] = 0
	T = T / np.maximum(1e-4, T.sum(0))

	path = [seed_idx]
	last_visited = seed_idx
	num_tid = len(tids)

	while len(path) < length:
		if T.sum() == 0:
			break

		next_track_probs = T[:,last_visited]
		if next_track_probs.sum() == 0:
			del path[-1]
			last_visited = path[-1]
			continue

		#next_track_probs += np.random.uniform(size=len(next_track_probs))
		#next_track_probs = next_track_probs / next_track_probs.sum()

		next_track = np.random.choice(range(num_tid), size=1, p=next_track_probs)[0]
		T[next_track,:] = 0
		T = T / np.maximum(1e-4, T.sum(0))

		path.append(next_track)
		last_visited = next_track

	print('Path of length %d traversed' % len(path))
	return path

def create_playlist(fov, seed):
	similar_pairs, tids = read_similair_pairs(fov)
	assert seed in tids, 'Must select a seed within the existing tids.'

	T = create_transition_matrix(similar_pairs, len(tids))
	path = traverse_graph(T, np.argwhere(tids == seed).ravel()[0], tids)

	tid_path = []
	for idx in path:
		tid_path.append(tids.index(idx))

	return tid_path

def print_playlist(playlist):
	for tid in playlist:
		title, artist = get_track_metadata(tid)
		print(f'{title} -- {artist}')


if __name__ == '__main__':
	fov = int(sys.argv[1])
	seed = sys.argv[2]

	playlist = create_playlist(fov, seed)
	print_playlist(playlist)