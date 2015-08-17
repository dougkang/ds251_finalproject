$(document).ready(function() {
      // Processing song name
      var serverName=jQuery.trim($('#hiddenServerName').text());
      var songNameList = jQuery.trim($('#hiddenSongNameList').text());
      var songs = songNameList.split(';');
      for (i = 0; i < songs.length; i++) { 
            $("#searchResults").append("<div class='songList'>" + songs[i] + "</div>");
            }
      
      // Getting song Ids
      var songIdList = jQuery.trim($('#hiddenSongIdList').text());
      var songIds = songIdList.split(';');
      
      $(".songList").click(function() {
            var songName = $(this).html();
            var songIndex = $(this).index();
            var trackId = songIds[songIndex];
            var myUrl = 'http://' + serverName + '/player?id=';
            var myUrl = myUrl.concat(trackId);
            window.open(myUrl);
            });
});