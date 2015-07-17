$(document).ready(function() {
    var input = $('#hiddenP').text();
    var trackIds = input.split(',');
 
    var i = 0;
    
    var artistTrackUrl = "http://localhost:8080/returnArtistAndTrackname?id=" + trackIds[i];
    artistTrackUrl = artistTrackUrl.replace(/\s/g, '');
    $.ajax({url: artistTrackUrl, success: function(result) {
            $('#artistAndTrackname').html(result);
            }
        });
    
    var artUrl = "http://localhost:8080/returnArtwork?id=" + trackIds[i];
    artUrl = artUrl.replace(/\s/g, '');
    $.ajax({url: artUrl, success: function(result) {
            $('img').attr("src", result);
            }
        });
    
    
    var trackUrl = "http://localhost:8080/returnClip?id=" + trackIds[i];
    trackUrl = trackUrl.replace(/\s/g, '');
    $.ajax({url: trackUrl, success: function(result) {
            $("source").attr("src", result);
            $('audio').load();
            }
        });
    
    $('audio').on('ended', function() {
        i = i + 1;
        
        var artistTrackUrl = "http://localhost:8080/returnArtistAndTrackname?id=" + trackIds[i];
        artistTrackUrl = artistTrackUrl.replace(/\s/g, '');
        $.ajax({url: artistTrackUrl, success: function(result) {
            $('#artistAndTrackname').html(result);
            }
        });
        
        var artUrl = "http://localhost:8080/returnArtwork?id=" + trackIds[i];
        artUrl = artUrl.replace(/\s/g, '');
        $.ajax({url: artUrl, success: function(result) {
            $('img').attr("src", result);
            }
        });
        
        trackUrl = "http://localhost:8080/returnClip?id=" + trackIds[i];
        trackUrl = trackUrl.replace(/\s/g, '');
        $.ajax({url: trackUrl, success: function(result) {
            $("source").attr("src", result);
            $('audio').load();
            }
        });
        });

    });
