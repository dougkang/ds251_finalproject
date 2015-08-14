from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q
import re
import os
import sys

client = Elasticsearch(['http://169.55.57.38:9200'])

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
# In[33]:

sim_file = '/root/ds251_finalproject/models/tqi_song_sim.csv'

#print get7DigitalID('TREDTHC128F92D42F0')
#print getTrackID(4759153)
#print getSimilars('TREDTHC128F92D42F0')
# In[91]:

def getSimilarSongs(tid, returnCount):
    #tid = 'TREDTHC128F92D42F0'
    data = getSimilars(tid)
    if data:
        #print '(total number of similar tracks: %d)' % (len(data.split(','))/2)
        data = str(data).replace('\\n','').replace(' ','').replace("u'","").replace("'","").replace('[','').replace(']','')
        data_unpacked = []
        for idx, d in enumerate(data.split(',')):
            if idx % 2 == 0:
                pair = [d]
            else:
                pair.append(float(d))
                data_unpacked.append(pair)

        # sort
        data_unpacked = sorted(data_unpacked, key=lambda x: x[1], reverse=True)

        returnList = []
        for k in range(returnCount):
            if k < len(data_unpacked) - 1:
                returnList.append(tuple(data_unpacked[k]))
        return returnList


# In[ ]:




# In[82]:

def getSimilarityPerc(pred_arr, real_arr):
    min_length = min(len(pred_arr), len(real_arr))
    #print min_length
    pred_sub_arr = pred_arr[:min_length]
    real_sub_arr = real_arr[:min_length]
    
    
    diff_count = float(len(set(real_sub_arr) - set(pred_sub_arr)))
    min_length = float(min_length)
    same_count = min_length - diff_count
    
    return same_count/min_length


# In[103]:

def procSong(pred_arr, real_arr):
    min_length = min(len(pred_arr), len(real_arr))
    pred_sub_arr = pred_arr[:min_length]
    real_sub_arr = real_arr[:min_length]
    
    same_count = len(list(set(real_sub_arr) & set(pred_sub_arr)))
    return same_count, min_length, len(pred_arr), len(real_arr)


# In[105]:

match = 0
match_over_rp = 0
match_over_real = 0
match_over_pred = 0

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

            #print sorted(set(pred_song_list))
            #print sorted(set(real_similar_song_list))
            #print getSimilarityPerc(pred_song_list, real_similar_song_list)
            same_count, rp_count, r_count, p_count = procSong(pred_song_list, real_similar_song_list)
            match += same_count
            match_over_rp += rp_count
            match_over_real += r_count
            match_over_pred += p_count
        #print '----------------------------------------'
        

fopen.close()
print float(match)/float(match_over_rp)
print float(match)/float(match_over_real)
print float(match)/float(match_over_pred)


