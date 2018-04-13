//check if summary tab is open
//if chart tab is active
//clear contents
//get chart
$(document).ready(function(){


  $('#summary-tab').click(function(){
    // $('.summary-chart').each(function(){
    //   console.log(this.children);
    // });
    // ;
    setTimeout(chartClick, 2000);
  });

  // console.log($element.html());


  //$('#js-chart-tab').hasClass('active') == true)

});

function chartClick(){
  $('#chart-tab').trigger('click');
}
