import pandas as pd
import numpy as np

import sys
import os
from os.path import join, isfile

from sputil import read_spcsv

def smoothing_kernel(fov):
	return np.ones(fov, dtype=np.float64) / (2**np.arange(fov))

def process_session(session, fov):
	kernel = smoothing_kernel(fov)
	fname = 'data/similar_pairs_fov%d.csv' % fov

	if not isfile(fname):
		f = open(fname, 'w')
		f.write('tid1,tid2,weight\n')
	else:
		f = open(fname, 'a')

	for i in range(0, len(session) - 2*fov + 1):
		base_tid = session.iloc[i,:].id
		
		for kernel_idx, j in enumerate(range(i+1, i+fov+1)):
			connected_tid = session.iloc[j,:].id
			weight = kernel[kernel_idx]

			f.write(f'{base_tid},{connected_tid},{weight}\n')

	f.close()

def get_session_idxs(times, durations):
	dts = times[1:] - times[:-1]
	diffs = np.abs(dts - durations[:-1])
	idxs = np.argwhere(diffs > 2*durations[:-1]).ravel()
	return np.concatenate((idxs, [len(times)]))

def read_rp_time_data(fov):
	sp_dir = os.environ['SPPATH']
	recents = read_spcsv(join(sp_dir, 'recently_played.csv'))
	recents = recents.sort_values('timestamp')
	times = np.array(recents.timestamp)

	if isfile('.last-f%d.txt' % fov):
		with open('.last-f%d.txt') as f:
			last_ts = int(f.read())
		
		mask = times>last_ts
		recents = recents.iloc[mask,:]

	with open('.last-f%d.txt' % fov, 'w') as f:
		f.write(str(int(times[-1])))

	return recents

if __name__ == '__main__':
	fov = 1
	if len(sys.argv) > 1:
		fov = int(sys.argv[1])

	recents = read_rp_time_data(fov)
	times = np.array(recents.timestamp)
	durations = np.array(recents.duration / 1000)

	splits = get_session_idxs(times, durations)
	last_split = 0

	for split in splits:
		if split - last_split > 1:
			session = recents.iloc[last_split:split,:]
			process_session(session, fov)
		last_split = split
