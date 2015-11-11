jQuery(document).ready(function() {
    App.init();

    // Select Multiple with checkboxes widget.
    //
    // By default all checkbox choices are hidden, except they are selected.
    // A click on the corresponding `Show all` link displays them all.
    $('.filter-form .select-multiple').each(function(){
        var $sel = $(this);

        $sel.find('span.show-all').show();

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

    var options = {
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
    }

    $('select[name*=organization]').selectize(options);

    $('textarea[name$=keywords]').selectize({
        delimiter: ',',
        persist: false,
        create: function(input) {
            return {
                value: input,
                text: input
            }
        }
    });
});
