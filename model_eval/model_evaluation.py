#!/usr/bin/python
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q
import re
import os
import sys

def die_with_usage():
    print 'USAGE:'
    print '  ./model_evaluation.py <songSim.csv>'
    sys.exit(0)

if len(sys.argv) != 2:
    die_with_usage()

# sanity check song_sim.csv file
sim_file = sys.argv[1]
if not os.path.isfile(sim_file):
    print 'ERROR: file %s does not exist?' % sim_file
    die_with_usage()

# connect to elastic search
client = Elasticsearch(['http://169.55.57.38:9200'])

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

# function to format and sort returned similar songs
def getSimilarSongs(tid, returnCount):
    data = getSimilars(tid)
    if data:
        data = str(data).replace('\\n','').replace(' ','').replace("u'","").replace("'","").replace('[','').replace(']','')
        data_unpacked = []
        for idx, d in enumerate(data.split(',')):
            if idx % 2 == 0:
                pair = [d]
            else:
                pair.append(float(d))
                data_unpacked.append(pair)

        # sort similar songs by similarity scores
        data_unpacked = sorted(data_unpacked, key=lambda x: x[1], reverse=True)

        returnList = []
        for k in range(returnCount):
            if k < len(data_unpacked) - 1:
                returnList.append(tuple(data_unpacked[k]))
        return returnList

# function to compare two similar song lists
def procSong(pred_arr, real_arr):
    min_length = min(len(pred_arr), len(real_arr))
    pred_sub_arr = pred_arr[:min_length]
    real_sub_arr = real_arr[:min_length]

    same_count = len(list(set(real_sub_arr) & set(pred_sub_arr)))
    return same_count, min_length, len(pred_arr), len(real_arr)


match = 0 # total number of matched similar songs
match_over_rp = 0 # total overlap lenth of real and predicted similar songs
match_over_real = 0 # total number of real similar songs
match_over_pred = 0 # total number of predicted similar songs

fopen = open(sim_file,'r')
lineCount = 0

for line in fopen:
    lineCount += 1
    line = line.strip('\n')
    lineArr = line.split(',')
    lineArr = map(lambda x:int(x),lineArr)
    seven_digital_id = lineArr[0]
    pred_song_list = lineArr[1:]

    exp_return_count = len(lineArr) - 1
    track_id = getTrackID(seven_digital_id)
    #print "lineCount: {}, 7digitalID: {}, TrackID: {}".format(lineCount, seven_digital_id, track_id)
    if track_id:
        similar_songs_n_score = getSimilarSongs(track_id, exp_return_count)

        if similar_songs_n_score:
            real_similar_song_list = map(lambda x:get7DigitalID(x[0]), similar_songs_n_score)

            same_count, rp_count, r_count, p_count = procSong(pred_song_list, real_similar_song_list)
            match += same_count
            match_over_rp += rp_count
            match_over_real += r_count
            match_over_pred += p_count

fopen.close()

print 'Total number of matched similar songs:', match
print 'Precision:', float(match)/float(match_over_pred)
print 'Recall:', float(match)/float(match_over_real)
print '(# total match) / (total overlap lenth of real and predicted similar songs):', float(match)/float(match_over_rp)

