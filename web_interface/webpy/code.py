import web
import py7D
import requests
import yaml
import json

serverName="169.53.76.112" # Server IP where Webapp is hosted

urls = (
    '/', 'search',
    '/player', 'player',
    '/returnClip', 'returnClip',
    '/returnArtwork', 'returnArtwork',
    '/returnArtistAndTrackname', 'returnArtistAndTrackname'
    )
render = web.template.render('templates/')

# Renders the Search page
class search:
    def GET(self):
        user_data = web.input(searchText=None)
        searchTerms = user_data.searchText
        if searchTerms == None:
            artist_and_track = ""
            id_7digital = ""
            searchTerms = ""
        else:
            # Query ElasticSearch based on search terms
            searchTerms = searchTerms.lower()
            artist_and_track, id_7digital = searchSongs(searchTerms)
        return render.search(artist_and_track, id_7digital, searchTerms, serverName)

# Renders the Music player page
class player:
    def GET(self):
        user_data = web.input()
        songId = user_data.id
        # Query ElasticSearch to get similar Songs
        artist_and_track, id_7digital = getSimilarTrackNameandIds(songId)
        return render.player(artist_and_track, id_7digital, serverName)

# Makes a call to 7Digital REST api
# Returns streaming URL based on a 7Digital_id
class returnClip:
    def GET(self):
        user_data = web.input()
        songId = user_data.id
        uri = py7D.preview_url(songId)
        response = requests.get(uri)
        if response.status_code == 200:
            return uri
        else:
            return 'static/notfound.mp3'

# Makes a call to 7Digital REST api
# Returns URL to the song art work
class returnArtwork:
    def GET(self):
        user_data = web.input()
        songId = user_data.id
        try:
            trackDetails = py7D.request('track', 'details', trackId=songId, imageSize=200, country='US')
        except:
            artwork = "static/artworknotfound.png"
        else:
            artwork = trackDetails.items()[0][1].items()[5][1].items()[9][1].items()[7][1]
        return artwork

# Makes a call to 7Digital REST api
# Returns Artist name, Track name and release date
class returnArtistAndTrackname:
    def GET(self):
        user_data = web.input()
        songId = user_data.id
        try:
            trackDetails = py7D.request('track', 'details', trackId=songId, imageSize=200, country='US')
        except:
            artist_and_track = "Artist and Track name not found @ 7Digital"
        else:
            songTitle = trackDetails.items()[0][1].items()[5][1].items()[1][1]
            artist = trackDetails.items()[0][1].items()[5][1].items()[3][1].items()[1][1]
            release_date = trackDetails.items()[0][1].items()[5][1].items()[9][1].items()[8][1].split('T')[0]
            artist_and_track = "Artist: " + artist + "<br/>" + "Track: " + songTitle + "<BR/>" + "Release date: " + release_date
        return artist_and_track

# This function queries Elastic Search
# Based on a 7Digital_id it queries ElasticSearch for
# similar songs
def getSimilarIds(songId):
    d1 = dict(); d1['head'] = songId
    d2 = dict(); d2['term'] = d1
    query = dict(); query['query'] = d2
    query = json.dumps(query)
    # ElasticSearch URI
    uri = "http://elastic:9200/similarsongs/fromspark/_search?format=yaml"
    # Call Rest API
    response = requests.get(uri, data=query)
    result = yaml.load(response.text.decode('ascii', 'ignore'))
    similar_song_ids = result['hits']['hits'][0]['_source']['similar']
    return similar_song_ids
    #return [songId] + [3408664, 5941421, 6292080, 3408662, 2746794, 1853509, 1127854]
    #return [songId] 

# Queries ElasticSearch
# Passes a list of 7Digital_Ids
# and obtains associated song names
def getSimilarTrackNameandIds(songId):
    # Creating terms Query
    similarIds = getSimilarIds(songId)
    # Creating query
    size = dict(); size['size'] = 25
    d1 = dict(); d1['id_7digital'] = similarIds
    d2 = dict(); d2['terms'] = d1
    d3 = dict(); d3['query'] = d2
    query = size
    query.update(d3)
    query = json.dumps(query)
    # ElasticSearch URI
    uri = "http://elastic:9200/artisttrack7digital/frommetadata/_search?format=yaml"
    # Call Rest API
    response = requests.get(uri, data=query)
    result = yaml.load(response.text.decode('ascii', 'ignore'))
    # Processing RestAPI output
    artist_and_track = list()
    id_7digital = list()
    for hit in result['hits']['hits']:
        artist_and_track.append(hit['_source']['artist_and_track'])
        id_7digital.append(hit['_source']['id_7digital'])
    return ';'.join(artist_and_track), ';'.join(id_7digital)

# Queries ElasticSearch based on Search terms entered by the user
# It returns list of song names and 7Digital track Ids
def searchSongs(searchTerms):
    # Creating terms Query
    searchTerms = searchTerms.encode('ascii', 'ignore').strip()
    terms = searchTerms.split()
    size = dict(); size['size'] = 50
    d1 = dict(); d1['artist_and_track'] = terms
    d2 = dict(); d2['terms'] = d1
    d3 = dict(); d3['query'] = d2
    query = size
    query.update(d3)
    query = json.dumps(query)
    # ElasticSearch URI
    uri = "http://elastic:9200/artisttrack7digital/frommetadata/_search?format=yaml"
    # Call Rest API
    response = requests.get(uri, data=query)
    result = yaml.load(response.text.decode('ascii', 'ignore'))
    # Processing RestAPI output
    artist_and_track = list()
    id_7digital = list()
    for hit in result['hits']['hits']:
        artist_and_track.append(hit['_source']['artist_and_track'])
        id_7digital.append(hit['_source']['id_7digital'])
    return ';'.join(artist_and_track), ';'.join(id_7digital)

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()

