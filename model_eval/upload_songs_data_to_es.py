#!/usr/bin/python

from elasticsearch import Elasticsearch
import requests
import yaml
import json

def main():
    es = Elasticsearch(['http://169.55.57.38:9200'])

    fhndlInput = open('/root/songs.csv', 'r')

    for i, line in enumerate(fhndlInput):
            # Processing line
            line = line.decode('ascii', 'ignore')
            line_split = line.split(',')

            track_id = line_split[0].strip()
            seven_digital_id = line_split[1].strip()

            # Creating json body
            body = dict()
            body['seven_digital_id'] = seven_digital_id
            body['track_id'] = track_id

            body = json.dumps(body)

            # Uploading to ElasticSearch
            retval = es.index(index="songs", doc_type='db', id=i+1, body=body)


    fhndlInput.close()
if __name__ == '__main__':
    main()
