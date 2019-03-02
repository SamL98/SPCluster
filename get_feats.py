import os
import pandas as pd

import spotipy.util as util
import requests

from lfuncs import lmap, lfilter

client_id = os.environ['SPOTIPY_CLIENT_ID']
client_secret = os.environ['SPOTIPY_CLIENT_SECRET']
redirect_uri = 'http://localhost:8080/callback'
token = util.prompt_for_user_token(
    'lerner98', 
    'user-read-recently-played user-library-read', 
    client_id=client_id,
    client_secret=client_secret, 
    redirect_uri=redirect_uri)

base_url = 'https://api.spotify.com/v1/'
trax_url = base_url + 'tracks'

def return_token():
    return token

def format_track(track):
    return { 
        'artist': '"' + track['artists'][0]['name'] + '"',
        'id': track['id'],
        'name': '"' + track['name'] + '"' 
    }

def get_tracks_by_ids(ids):
    r = requests.get(
        trax_url, 
        params={'ids': ','.join(ids)},
        headers={'Authorization': 'Bearer ' + token})

    if not 'tracks' in r.json():
        return []

    tracks = (r.json())['tracks']
    tracks = lmap(format_track, tracks)
    return tracks

def format_features(feat):
    return [
        feat['danceability'], 
        feat['energy'], 
        feat['speechiness'], 
        feat['acousticness'], 
        feat['instrumentalness'], 
        feat['liveness'], 
        feat['valence'],
        feat['loudness'],
        str(float(int(feat['mode']))),
        feat['tempo']
    ]

def get_features(seg):
    global token

    url = 'https://api.spotify.com/v1/audio-features'
    params={ 'ids': ','.join(seg[:min(100, len(seg))]) }
    r = requests.get(
        url, 
        params=params, 
        headers={'Authorization': 'Bearer ' + token})

    feats = lfilter(lambda x: not x is None, r.json()['audio_features'])
    feats = lmap(format_features, feats)

    if len(seg) < 100:
	    return feats
    else:
        feats.extend(get_features(seg[100:]))
        return feats

def get_track_by_id(id):
    r = requests.get(trax_url + '/' + id, headers={'Authorization': 'Bearer ' + token})
    return format_track(r.json())

def get_library_features():
    df = pd.read_csv('library.csv')
    ids = df['id'].tolist()

    f = open('features_full.csv', 'w')
    f.write('id,danceability,energy,speechiness,acousticness,instrumentalness,liveness,valence\n')

    features = get_features(ids)
    for tid, feat in zip(ids, features):
        feat = [tid] + feat
        f.write(','.join([str(x) for x in feat]) + '\n')

if token:
	get_library_features()
else:
    print('Could not get spotipy token')