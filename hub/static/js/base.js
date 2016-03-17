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
    updateOrgDropdowns(); // from selectize-dropdowns.js
    
    // -------------------------------------------------------------------------
    // Tagging (Keywords)
    // -------------------------------------------------------------------------
    updateTagFilterDropdowns(); // from selectize-dropdowns.js
});
