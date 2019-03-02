from sputil import get_tracks, read_spcsv, fetch_library
import pandas as pd
import os
from os.path import join

recents = read_spcsv(join(os.environ['SPPATH'], 'recently_played.csv'))
library = fetch_library()

tids_to_fetch = []
tracks = []

for _, row in recents.iterrows():
    lib_rows = library.loc[lambda t: t.id == row.id]
    if len(lib_rows) > 0:
        continue
    tids_to_fetch.append(row.id)

nt = 50
for i in range(len(tids_to_fetch)//nt):
    tids = tids_to_fetch[i*nt:(i+1)*nt]
    track_batch = get_tracks(tids)
    if track_batch is None:
        continue
    tracks.extend(track_batch)

pd.DataFrame(tracks).to_csv('other_tracks.csv')