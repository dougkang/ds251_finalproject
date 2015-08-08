#!/bin/bash

cd /tmp
for x in {A..Z}; do
  fn="$x.tar.gz"
  echo "downloading $fn"
  rsync -avzuP "publicdata.opensciencedatacloud.org::ark:/31807/osdc-c1c763e4/$fn" "/tmp/$fn"
  tar xzvf $fn
  echo "extracting features from $x"
  find $x/ -type f -name *.h5 | \
    xargs -I{} python preproc/msongsdb/extract_features.py {} artist_id artist_mbid \
      artist_terms song_id track_7digitalid track_id year danceability duration energy key loudness \
      mode sections_start segments_start segments_loudness_max segments_pitches segments_timbre tempo \
      time_signature > $out
  out="$x.feat"
  echo "putting /millionSongFeats/$out"
  /usr/local/hadoop/bin/hdfs dfs -put $out /millionSongFeats/$x
  echo "cleaning up"
  rm -r $x $fn $out
done

line=$1
