/*

    General Javascript, applied on all pages

*/
jQuery(document).ready(function() {

    // -------------------------------------------------------------------------
    // Bootstrap Theme Init
    // -------------------------------------------------------------------------
    App.init();

    // Set a URL fragment for each Bootstrap3 tab on change, and automatically
    // show that tab on load.
    $(function(){
        var hash = window.location.hash.replace('-panel', '');

        hash && $('ul.nav a[href="' + hash + '"]').tab('show');
        $('.nav-tabs a').click(function (e) {
            $(this).tab('show');
            window.location.hash = this.hash + '-panel';
        });
    });

    // -------------------------------------------------------------------------
    // Init Organizations Ajax dropdown
    // -------------------------------------------------------------------------
    $.updateOrgDropdowns();
});

// -------------------------------------------------------------------------
// Organizations Ajax dropdown
// Extracted to be available for calls outside of ready
// -------------------------------------------------------------------------
jQuery.updateOrgDropdowns = function() {
  $('select[name*=organization]').selectize({
      valueField: 'pk',
      labelField: 'org_name',
      searchField: 'org_name',
      load: function(query, callback) {
          if (!query.length || query.length < 2) return callback();
          $.ajax({
              url: '/api/v1/organizations/',
              type: 'GET',
              dataType: 'json',
              data: {
                  q: query
              },
              error: function() {
                  callback();
              },
              success: function(res) {
                  callback(res);
              }
          });
      }
  });
};
