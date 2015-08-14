import sqlite3
import sys

simdbfile = '/home/hadoop/lastfm_similars.db'
simconn = sqlite3.connect(simdbfile)

trackdbfile = '/home/hadoop/track_metadata.db'
trackconn = sqlite3.connect(trackdbfile)

print "dump all data from track_metadata.db"
sql = "SELECT track_id, track_7digitalid FROM songs"
res = trackconn.execute(sql)
data = res.fetchall()
fopen = open("songs.csv","w")
for d in data:
    fopen.write("{},{}\n".format(d[0], d[1]))
fopen.close()



print "dump all data from lastfm_similars.db"
songopen = open("songs.csv","r")
fopen = open("similars_src.csv","w")
for s in songopen:
    tid = s.split(',')[0]
    sql_sim="SELECT tid, target FROM similars_src WHERE tid='{}'".format(tid)
    res_sim = simconn.execute(sql_sim)
    data_sim = res_sim.fetchall()
    for d in data_sim:
        fopen.write("{},{}\n".format(d[0], d[1]))
fopen.close()


simconn.close()
trackconn.close()
