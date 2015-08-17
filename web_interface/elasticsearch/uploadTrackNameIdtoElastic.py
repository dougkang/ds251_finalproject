#!/usr/bin/python

from elasticsearch import Elasticsearch
import json
import requests
import yaml

input_file = 'track_meta.csv'

def querySimilarSongs(song_id):
    # Creating query
    d1 = dict(); d1['head'] = song_id
    d2 = dict(); d2['term'] = d1
    query = dict(); query['query'] = d2
    query = json.dumps(query)
    # ElasticSearch URI
    uri = "http://elastic:9200/similarsongs/fromspark/_search?format=yaml"
    # Call Rest API
    response = requests.get(uri, data=query)
    result = yaml.load(response.text.decode('ascii', 'ignore'))
    # Return RestAPI output
    return result['hits']['total']

def main():
    es = Elasticsearch('elastic')
    fhndlInput = open(input_file, 'r')
    j = 0
    for i, line in enumerate(fhndlInput):
            # Processing line
            line = line.decode('ascii', 'ignore')
            line = line.replace('"', '')
            line = line.replace("'", '')
            line_split = line.split(',')
            
            id_7digital = line_split.pop().strip()
            artist_and_track = ','.join(line_split)

            # Creating json body
            body = dict()
            body['artist_and_track'] = artist_and_track
            body['id_7digital'] = id_7digital

            body = json.dumps(body)

            # Uploading to ElasticSearch
            if querySimilarSongs(id_7digital) != 0:
                j = j + 1
                retval = es.index(index="artisttrack7digital", doc_type='frommetadata', id=j, body=body)

    fhndlInput.close()

if __name__ == '__main__':
    main()



