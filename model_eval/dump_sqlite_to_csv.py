#!/usr/bin/python
import os
import sqlite3
import sys

def die_with_usage():
    print 'USAGE:'
    print '  ./dump_sqlite_to_csv.py <lastfm_similars.db> <track_metadata.db>'
    sys.exit(0)

if len(sys.argv) != 3:
    die_with_usage()

# sanity check db files
simdbfile = sys.argv[1]
trackdbfile = sys.argv[2]

if not os.path.isfile(simdbfile):
    print 'ERROR: db file %s does not exist?' % simdbfile
    die_with_usage()
if not os.path.isfile(trackdbfile):
    print 'ERROR: db file %s does not exist?' % trackdbfile
    die_with_usage()

# open connections
simconn = sqlite3.connect(simdbfile)
trackconn = sqlite3.connect(trackdbfile)

# dump track_id ~ track_7digitalid pairs to a file
print "dump track_id ~ track_7digitalid pairs from track_metadata.db"
sql = "SELECT track_id, track_7digitalid FROM songs"
res = trackconn.execute(sql)
data = res.fetchall()
fopen = open("songs.csv","w")
for d in data:
    fopen.write("{},{}\n".format(d[0], d[1]))
fopen.close()

# dump similar songs information to a file
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

# close connections
simconn.close()
trackconn.close()
