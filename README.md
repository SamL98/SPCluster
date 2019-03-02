# SPCluster

SPCluster uses graph clustering to create tailored playlists based on your listening history.

## Data Source

I set up a cron job on my laptop that periodically gets my recently played songs from Spotify. Spotify only lets you get the 50 most recent songs, so I have it set to run every few hours.

The job has been running on and off for about a month and I've gathered a little under 2500 tracks.

## Getting Adjacent Songs

Since I store all the songs in a large CSV file, I need a way of determining whether or not two adjacent songs came from the same sitting. To do this, I just see whether the difference in their timestamps are greater than twice the first songs duration. Simple but effective.

## Creating the Graph

In order to perform the graph clustering, I need to define the graph. I started to write a simple CLI to prompt me to respond if two random songs from my library are similar but I quickly realized that would take too long.

Therefore, I just build the graph edges from my listening history.

### Defining the FOV

Initially, I was just creating edges between tracks that were listened to back-to-back. However, then I realized that maybe I could do some data augmentation and define an edge between track that were two or more songs apart. This is the FOV - how many tracks ahead of the current one to add an edge for.

### Weighting the Edges

I believe it is less likely that a track further ahead of the current one will be similar, so I weight each edge exponentially by its distance to the current track, i.e. the track directly after the current one gets a weight of 1, the next 0.5, the next 0.25, and so on.

## Clustering the Graph

Once the weighted, directed graph is defined, I can cluster it using MCL. I ran my personal implementation of MCL with p and e equal to 2 and for a max of 100 iterations (in case it didn't converge).

Interestingly enough, the clusters (playlists) with an FOV of one appear the best via inspection.