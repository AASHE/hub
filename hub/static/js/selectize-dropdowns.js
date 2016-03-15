// -------------------------------------------------------------------------
// Organizations Ajax dropdown
// Extracted to be available for calls outside of ready
// -------------------------------------------------------------------------
updateOrgDropdowns = function() {
  $('select[name*=organization]').selectize({
      valueField: 'pk',
      labelField: 'org_name',
      searchField: 'org_name',
      dropdownParent: 'body',
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

updateTagDropdowns = function() {
  $('input[name*=keywords]').selectize({
      delimiter: ',',
      persist: false,
      create: function(input) {
          return {
              name: input,
              text: input
          }
      },
      valueField: 'name',
      labelField: 'name',
      searchField: 'name',
      dropdownParent: 'body',
      load: function(query, callback) {
        if (!query.length || query.length <= 2) return callback();
        $.ajax({
            url: '/api/v1/tags/',
            type: 'GET',
            dataType: 'json',
            data: {
                q: query
            },
            error: function() {
                callback();
            },
            success: function(res) {
                console.log("success!");
                callback(res);
            }
        });
      }
  });
}
