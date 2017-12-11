//JS for the toolkit page
$( document ).ready(function() {


  checkForLock();


});

function checkForLock(){

  $('.lock-or-star').each(function(){

    if($(this).children().hasClass('icon-warning') == 0){
      $(this).append("<i class='fa fa-star-o rounded'></i>");
    }

  });
  
}
