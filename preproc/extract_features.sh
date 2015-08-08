#!/bin/bash

mkdir /data/tmp
cd /data/tmp
while read -r x; do
  fn="$x.tar.gz"
  out="$x.feat"
  echo "downloading $fn"
  rsync -avzuP "publicdata.opensciencedatacloud.org::ark:/31807/osdc-c1c763e4/$fn" "$fn"
  tar xzvf $fn
  echo "extracting features from $x"
  find . -type f -name *.h5 | \
    xargs -I{} python /root/ds251_finalproject/preproc/msongsdb/extract_features.py {} artist_id artist_mbid \
      artist_terms song_id track_7digitalid track_id year danceability duration energy key loudness \
      mode sections_start segments_start segments_loudness_max segments_pitches segments_timbre tempo \
      time_signature > $out
  echo "putting /millionSongFeats/$out"
  /usr/local/hadoop/bin/hdfs dfs -put $out /millionSongFeat/
  echo "cleaning up"
  rm -r $x $fn $out
done
