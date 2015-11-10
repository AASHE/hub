jQuery(document).ready(function() {
    App.init();

    // Select Multiple with checkboxes widget.
    //
    // By default all checkbox choices are hidden, except they are selected.
    // A click on the corresponding `Show all` link displays them all.
    $('.select-multiple').each(function(){
        var $sel = $(this);

        // Hide all non-checked items by default
        $sel.find('input[type=checkbox]:not(:checked)').each(function(){
            $(this).closest('li').hide();
        });

        // If all fields are checked, hide the select-all link
        if($sel.find('input[type=checkbox]:not(:checked)').length === 0) {
            $('.select-multiple-header span.show-all', $sel).hide();
            $('.select-multiple-header .select-all', $sel).show();
        }

        // Click on the 'show all' header will display them again
        $('.select-multiple-header span.show-all', $sel).click(function(){
            $sel.find('li:hidden').slideDown('fast');
            $(this).parent().find('.select-all').show();
            $(this).hide();
        });

        // Select all button
        $('.select-multiple-header span.select-all', $sel).click(function(){
            var $con = $(this).parents('section');
            var $ckb = $con.find('input[type=checkbox]');

            // If all items were already select, deselect them.
            if($con.find('input[type=checkbox]:checked').length === $ckb.length) {
                $ckb.attr('checked', false);
            } else {
                $ckb.attr('checked', true);
            }
        });
    });

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
