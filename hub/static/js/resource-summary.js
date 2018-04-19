//check if summary tab is open
//if chart tab is active
//clear contents
//get chart
$(document).ready(function(){


  $('#summary-tab').click(function(){
    setTimeout(chartClick, 2000);
  });

});

function chartClick(){
  $('#chart-tab').trigger('click');
}
