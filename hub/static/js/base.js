jQuery(document).ready(function() {
    App.init();

    // $('select:not(#id_organizations)').select2({
    //     minimumResultsForSearch: 20
    // });

    // $("#id_organizations").select2({
    //     ajax: {
    //         url: "/api/organizations",
    //         dataType: 'json',
    //         delay: 250,
    //         placeholder: "Type to find organization",
    //         data: function (params) {
    //             return {q: params };
    //         },
    //         processResults: function (data, page) {
    //             return {results: data};
    //         },
    //         cache: true
    //     },
    //     escapeMarkup: function (markup) {
    //         return markup;
    //     },
    //     data: [{ id: 0, text: 'enhancement' }, { id: 1, text: 'bug' }, { id: 2, text: 'duplicate' }, { id: 3, text: 'invalid' }, { id: 4, text: 'wontfix' }],
    //     minimumInputLength: 2,
    //     theme: 'classic',
    //     multiple: true
    // });

});
