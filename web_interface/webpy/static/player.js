$(document).ready(function() {
    // Displaying simillar songs
    var serverName=jQuery.trim($('#hiddenServerName').text());
    var songNameList = jQuery.trim($('#hidden_artist_and_track').text());
    var songs = songNameList.split(';');
    for (j = 0; j < songs.length; j++) { 
          $("#displaySimilarSongs").append("<div class='songList'>" + songs[j] + "</div>");
          }
    
    // Processing TrackIds
    var input = $('#hidden_id_7digital').text();
    var trackIds = input.split(';');
    var i = 0;
    
    // Playing first Song
    var artistTrackUrl = "http://" + serverName + "/returnArtistAndTrackname?id=" + trackIds[i];
    artistTrackUrl = artistTrackUrl.replace(/\s/g, '');
    $.ajax({url: artistTrackUrl, success: function(result) {
            $('#artistAndTrackname').html(result);
            }
        });
    
    var artUrl = "http://" + serverName + "/returnArtwork?id=" + trackIds[i];
    artUrl = artUrl.replace(/\s/g, '');
    $.ajax({url: artUrl, success: function(result) {
            $('img').attr("src", result);
            }
        });

    var trackUrl = "http://" + serverName + "/returnClip?id=" + trackIds[i];
    trackUrl = trackUrl.replace(/\s/g, '');
    $.ajax({url: trackUrl, success: function(result) {
            $("source").attr("src", result);
            $('audio').load();
            if (result == "static/notfound.mp3") {
                $('#messageDisplay').html('7Digital Responded - Track not found');
                $("div div:nth-child(" + 1 + ")").css("background-color", "#B7B8BA");
                } else { 
                $('#messageDisplay').html(' ');
                }
            
            }
        });
    
    // Playing next song after the current track ends
    $('audio').on('ended', function() {
        i = i + 1;
        
        if (i >= trackIds.length) {
            $('audio').pause();
        }
        
        var artistTrackUrl = "http://" + serverName + "/returnArtistAndTrackname?id=" + trackIds[i];
        artistTrackUrl = artistTrackUrl.replace(/\s/g, '');
        $.ajax({url: artistTrackUrl, success: function(result) {
            $('#artistAndTrackname').html(result);
            }
        });
        
        var artUrl = "http://" + serverName + "/returnArtwork?id=" + trackIds[i];
        artUrl = artUrl.replace(/\s/g, '');
        $.ajax({url: artUrl, success: function(result) {
            $('img').attr("src", result);
            }
        });
        
        trackUrl = "http://" + serverName + "/returnClip?id=" + trackIds[i];
        trackUrl = trackUrl.replace(/\s/g, '');
        $.ajax({url: trackUrl, success: function(result) {
            $('source').attr('src', result);
            $('audio').load();
            if (result == "static/notfound.mp3") {
                $('#messageDisplay').html('7Digital Responded - Track not found');
                ind = i+1;
                $("div div:nth-child(" + ind + ")").css("background-color", "#B7B8BA");
                } else { 
                $('#messageDisplay').html(' ');
                }
            }
            });
        });
    });
