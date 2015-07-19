import web
import py7D

urls = (
    '/', 'index',
    '/song', 'song',
    '/player', 'player',
    '/getTrackIds', 'getTrackIds',
    '/returnClip', 'returnClip',
    '/returnArtwork', 'returnArtwork',
    '/returnArtistAndTrackname', 'returnArtistAndTrackname'
    )
render = web.template.render('templates/')

class index:
    def GET(self):
        return render.index()

class song:
    def GET(self):
        user_data = web.input()
        songId = user_data.id
        songUrl = py7D.preview_url(songId)
        
        trackDetails = py7D.request('track', 'details', trackId=songId, imageSize=350, country='US')
        songTitle = trackDetails.items()[0][1].items()[5][1].items()[1][1]
        artist = trackDetails.items()[0][1].items()[5][1].items()[3][1].items()[1][1]
        artwork = trackDetails.items()[0][1].items()[5][1].items()[9][1].items()[7][1]
        return render.song(songUrl, songTitle, artist, artwork)

class player:
    def GET(self):
        user_data = web.input()
        songId = user_data.id
        tracks = getTrackIds(songId)
        tracks = ','.join(tracks)
        return render.player(tracks)

class returnClip:
    def GET(self):
        user_data = web.input()
        songId = user_data.id
        return py7D.preview_url(songId)

class returnArtwork:
    def GET(self):
        user_data = web.input()
        songId = user_data.id

        trackDetails = py7D.request('track', 'details', trackId=songId, imageSize=350, country='US')
        artwork = trackDetails.items()[0][1].items()[5][1].items()[9][1].items()[7][1]
        return artwork

class returnArtistAndTrackname:
    def GET(self):
        user_data = web.input()
        songId = user_data.id

        trackDetails = py7D.request('track', 'details', trackId=songId, imageSize=350, country='US')
        songTitle = trackDetails.items()[0][1].items()[5][1].items()[1][1]
        artist = trackDetails.items()[0][1].items()[5][1].items()[3][1].items()[1][1]
        return "Artist: " + artist + "<br/>" + "Track: " + songTitle

def getTrackIds(id):
    # Use id variable later to query a database to randomly select Kmeans
    return ['9522', '8220', '9422', '9418']   

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()

