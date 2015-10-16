jQuery(document).ready(function() {
    App.init();

// $('select:not(#id_organizations)').select2({
//     minimumResultsForSearch: 20
// });

$("#id_organizations").select2({
  ajax: {
    url: "/api/organizations",
    dataType: 'json',
    delay: 250,
    placeholder: "Type to find organization",

      data: function (params) {
        var queryParameters = {
          q: params
        }
        return queryParameters;
      },
    processResults: function (data, page) {
      // parse the results into the format expected by Select2.
      // since we are using custom formatting functions we do not need to
      // alter the remote JSON data
      return {
        results: data
      };
    },
    cache: true
  },
  escapeMarkup: function (markup) { return markup; }, // let our custom formatter work
  minimumInputLength: 2,
});

});
