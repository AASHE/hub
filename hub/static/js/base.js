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
        valueField: 'id',
        labelField: 'text',
        searchField: 'text',
        load: function(query, callback) {
            if (!query.length) return callback();
            $.ajax({
                url: '/api/organizations/',
                type: 'GET',
                dataType: 'json',
                data: {
                    q: query,
                    additionalDataIfRequired: 'Additional Data'
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
