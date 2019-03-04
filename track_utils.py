from os.path import isfile
import atexit
from sputil import read_spcsv, get_track, fetch_library

misc_track_fname = 'other_tracks.csv'
init_misc_track_len = None
misc_tracks = None
lib = None

def load_lib():
	global lib
	lib = fetch_library()

def load_other_tracks():
	global misc_track_fname, init_misc_track_len, misc_tracks

	misc_tracks = pd.DataFrame(columns=library.columns)

	if isfile(misc_track_fname):
		misc_tracks = read_spcsv(misc_track_fname)

	init_misc_track_len = len(misc_tracks)

def save_other_tracks():
	global misc_track_fname, init_misc_track_len, misc_tracks

	if misc_tracks is None:
		return

	if init_misc_track_len is None or len(df) > init_misc_track_len:
		misc_tracks.to_csv(misc_track_fname)

atexit.register(save_other_tracks)

def get_track_metadata(tid):
	global misc_tracks, lib

	if lib is None:
		load_lib()

	if misc_tracks is None:
		load_other_tracks()

	rows = lib.loc[lambda t: t.id == tid]

	if len(rows) == 0:
		rows = misc_tracks.loc[lambda t: t.id == tid]

		if len(rows) == 0:
			track = get_track(tid)
			if track is None: 
				return

			title, artist = track['title'], track['artist']
			misc_tracks.append(track, ignore_index=True)
		else:
			row = rows.iloc[0,:]
			title, artist = row.title, row.artist
	else:
		row = rows.iloc[0,:]
		title, artist = row.title, row.artist

	return title, artist