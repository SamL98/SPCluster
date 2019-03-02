import atexit
import subprocess
from numpy.random import choice
from sputil import fetch_library

def close_files():
	global true_f, false_f
	if not true_f is None:
		true_f.close()
	if not false_f is None:
		false_f.close()

def play_track(tid):
	as_str = '\'tell application "Spotify" to play track "spotify:track:%s"\'' % tid
	subprocess.call('osascript -e ' + as_str, shell=True)

def print_track(t):
	t_len = max(len(t.title), len(t.artist))
	header_str = ''.join(['-'] * (t_len+3))
	title_pad = ''.join([' '] * (t_len - len(t.title)))
	artist_pad = ''.join([' '] * (t_len - len(t.artist)))

	print(header_str)
	print('| %s%s |' % (t.title, title_pad))
	print('| %s%s |' % (t.artist, artist_pad))
	print(header_str)
	print('')
	

if __name__ == '__main__':
	lib = fetch_library()
	lib_idxs = list(range(len(lib)))

	true_f = open('data/similar_pairs.txt', 'a')
	false_f = open('data/disimilar_pairs.txt', 'a')
	atexit.register(close_files)

	prompt = 'Yes [y] \nNo [n] \nPlay 1 [z] \nPlay 2 [x]: '
	play_commands = ['z', 'x']

	while True:
		idxs = choice(lib_idxs, 2, replace=False)
		t1, t2 = lib.iloc[idxs[0],:], lib.iloc[idxs[1],:]

		print_track(t1)
		print_track(t2)

		response = None
		while not (response == 'y' or response == 'n'):
			response = input(prompt).lower()

			if response in play_commands:
				tracks = [t1, t2]
				track = tracks[play_commands.index(response)]
				play_track(track.id)
				print('')
			elif response == '': 
				response = 'n'

		if response == 'y':
			true_f.write('%s,%s\n' % (t1.id, t2.id))
		elif response == 'n':
			false_f.write('%s,%s\n' % (t1.id, t2.id))

		print('\n')

	f.close()
