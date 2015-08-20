#!/usr/bin/python
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q
import re
import os
import sys
import datetime

print 'start time: ', datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def die_with_usage():
    print 'USAGE:'
    print '  ./model_evaluation.py <songList.csv>'
    sys.exit(0)

if len(sys.argv) != 2:
    die_with_usage()

# sanity check song_sim.csv file
sim_file = sys.argv[1]
if not os.path.isfile(sim_file):
    print 'ERROR: file %s does not exist?' % sim_file
    die_with_usage()

# connect to elastic search
client = Elasticsearch(['http://169.53.76.104:9200'])

# functions to query elastic search
def get7DigitalID(tid):
    s = Search(using=client, index="songs") \
        .query("match", track_id=tid)
    response = s.execute()
    return response[0].seven_digital_id

def getTrackID(seven_digital_id):
    s = Search(using=client, index="songs") \
        .query("match", seven_digital_id=seven_digital_id)
    response = s.execute()
    return response[0].track_id

def getSimilars(tid):
    s = Search(using=client, index="similars_src") \
        .query("match", track_id=tid)
    response = s.execute()
    if response:
        return response[0].similars

def getRcmds(seven_digital_id):
    s = Search(using=client, index="similarsongs") \
        .query("match", head=seven_digital_id)
    response = s.execute()
    if response:
        return response[0].similar

# function to format and sort returned similar songs
def getSimilarSongs(tid):
    data = getSimilars(tid)
    if data:
        return data[0::2]

# function to compare two similar song lists
def procSong(pred_arr, real_arr):
    same_count = len(list(set(real_arr) & set(pred_arr)))
    return same_count, len(pred_arr), len(real_arr)

match = 0 # total number of matched similar songs
match_over_real = 0 # total number of real similar songs
match_over_pred = 0 # total number of predicted similar songs

fopen = open(sim_file,'r')
lineCount = 0

for line in fopen:
    lineCount += 1
    line = line.strip('\n')
    seven_digital_id = line

    track_id = getTrackID(seven_digital_id)
    '''
    if (lineCount % 1000) == 0:
        print lineCount
        print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
    '''
    if track_id:
        similar_songs_n_score = getSimilarSongs(track_id)

        if similar_songs_n_score:
            pred_song_list = getRcmds(seven_digital_id)
            if not pred_song_list:
                continue
            pred_song_list = map(lambda x: getTrackID(x), pred_song_list)

            same_count, r_count, p_count = procSong(pred_song_list, similar_songs_n_score)

            match += same_count
            match_over_real += r_count
            match_over_pred += p_count

fopen.close()

print 'Total number of matched similar songs:', match
print 'Precision:', float(match)/float(match_over_pred)
print 'Recall:', float(match)/float(match_over_real)

print 'end time:', datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
