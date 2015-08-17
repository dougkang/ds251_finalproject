#!/usr/bin/python

from elasticsearch import Elasticsearch
import json

input_file = 'songSim.csv'

def main():
    es = Elasticsearch('elastic')
    fhndlInput = open(input_file, 'r')
    j = 0
    
    for i, line in enumerate(fhndlInput):
        cols = line.strip().split(',')
        if len(cols) >=26:
            head = cols[0]
            similar = cols[1:26]

            # Creating json body
            body = dict()
            body['head'] = head
            body['similar'] = similar

            body = json.dumps(body)

            # Uploading to ElasticSearch
            j = j + 1
            retval = es.index(index="similarsongs", doc_type='fromspark', id=j, body=body)

    fhndlInput.close()

if __name__ == '__main__':
    main()



