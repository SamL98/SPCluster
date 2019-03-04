import sys
import numpy as np
import matplotlib.pyplot as plt

from sputil import get_rex, get_feats_for_tracks
from create_playlist import create_playlist
from track_utils import *

def get_feature_statistics(features):
    features = dict()
    for key, 
    
    return features.mean(0), features.std(0)

def analyze_playlist(fov, tid):
    my_playlist = create_playlist(fov, tid)
    my_feats = get_feats_for_tracks(my_playlist)
    my_mean, my_var = get_feature_variance(my_feats)

    sp_playlist = get_rex(tid, limit=10)
    sp_feats = get_feats_for_tracks(sp_playlist)
    sp_mean, sp_var = get_feature_variance(sp_feats)

    return (my_mean, my_var), (sp_mean, sp_var)

if __name__ == '__main__':
    fov = int(sys.argv[1])

    test_tids = [
        '58yWJFglBzvZ7Zao70lGtJ'
        '1cZ7NCXlGhz4RTGgLHZ7Ow'
    ]

    for tid in test_tids:
        my_stats, sp_stats = analyze_playlist(fov, tid)