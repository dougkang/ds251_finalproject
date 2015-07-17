import py7D

def main():
    inputFile = "trackIds.txt"
    fhndlInput = open('trackIds.txt', 'r')
    fhndlOutput = open('static/ArtistandTracks.csv', 'w')
    fhndlOutput.write('"track","trackId"' + '\n')
    
    for line in fhndlInput:
        songId = line.strip()
        trackDetails = py7D.request('track', 'details', trackId=songId, imageSize=350, country='US')
        songTitle = trackDetails.items()[0][1].items()[5][1].items()[1][1]
        artist = trackDetails.items()[0][1].items()[5][1].items()[3][1].items()[1][1]
        song_artist = artist + ", " + songTitle
        outLine = '"' + song_artist + '","' + songId + '"' 
        print outLine
        fhndlOutput.write(outLine + '\n')
    fhndlInput.close()
    fhndlOutput.close()




if __name__ == '__main__':
    main()
