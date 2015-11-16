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
        var hash = window.location.hash;
        hash && $('ul.nav a[href="' + hash + '"]').tab('show');
        $('.nav-tabs a').click(function (e) {
            $(this).tab('show');
            var scrollmem = $('body').scrollTop();
            window.location.hash = this.hash;
            $('html,body').scrollTop(scrollmem);
        });
    });

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
