/*

    General Javascript, applied on all pages

*/
jQuery(document).ready(function() {
    // Bootstrap Theme Init
    App.init();

    // -------------------------------------------------------------------------
    // Organizations Ajax dropdown
    // -------------------------------------------------------------------------
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
});
