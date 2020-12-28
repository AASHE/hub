$(document).ready(function(){

  checkForVideos();

});

function checkForVideos(){
  if (!$('.embed-responsive').length){
    $('#embedded-videos').append('<p>No videos provided in a supported format</p>')
  }
}
