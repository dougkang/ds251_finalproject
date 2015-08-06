#!/bin/bash

while read line; do
  out=`echo $line | cut -d/ -f3- | sed 's/\//-/g'`
  echo "reading $line, writing to /millionSongFeats/$out"
  /usr/local/hadoop/bin/hdfs dfs -get $line /tmp/song.h5
  python preproc/msongsdb/extract_features.py /tmp/song.h5 artist_id artist_mbid \
    artist_terms song_id track_7digitalid track_id year danceability duration energy key loudness \
    mode sections_start segments_start segments_loudness_max segments_pitches segments_timbre tempo \
    time_signature > /tmp/song.feat
  /usr/local/hadoop/bin/hdfs dfs -put /tmp/song.feat /millionSongFeats/$out
  rm /tmp/song.h5 /tmp/song.feat
done

echo "completed!"
