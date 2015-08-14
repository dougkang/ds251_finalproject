#!/usr/bin/python

from elasticsearch import Elasticsearch
import requests
import yaml
import json

def main():
    es = Elasticsearch(['http://169.55.57.38:9200'])

    fhndlInput = open('/root/similars_src.csv', 'r')

    for i, line in enumerate(fhndlInput):
            # Processing line
            line = line.decode('ascii', 'ignore')
            line_split = line.split(',')

            track_id = line_split[0].strip()
            similars = line_split[1:]

            # Creating json body
            body = dict()
            body['track_id'] = track_id
            body['similars'] = similars

            body = json.dumps(body)

            # Uploading to ElasticSearch
            retval = es.index(index="similars_src", doc_type='db', id=i+1, body=body)


    fhndlInput.close()
if __name__ == '__main__':
    main()
