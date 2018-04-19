/*

    Filter Form Javascript

*/
jQuery(document).ready(function() {
    // -------------------------------------------------------------------------
    // The State field is only visible if the US or CA country is selected
    // -------------------------------------------------------------------------
    var $country = $('#id_country');
    var $state = $('.filter-form .select-multiple.field_id_state');
    var $province = $('.filter-form .select-multiple.field_id_province');

    var collapseStateForm = function(obj, collapse) {
        if(collapse) {
            obj.find('input[type=checkbox]').each(function(){
                $(this).closest('li').slideUp('fast');
                $(this).attr('checked', false);
            });
            obj.hide();
        }
        else {
            obj.find('li:hidden').slideDown('fast');
            obj.find('.select-all').show();
            obj.find('.show-all').hide();
            obj.find('.hide-unselected').show();
            obj.show();
        }
    }

    var showHideStateForm = function() {
        var val = $country.val();

        if(val === undefined) return;

        collapseStateForm($province, val != 'CA');
        collapseStateForm($state, val != 'US');
    }

    $country.on('change', showHideStateForm)
    showHideStateForm();

    // -----------------------------------------------------------------------
    // Add some description here
    // -----------------------------------------------------------------------
    $('#summary-tab').click(function(){
      setTimeout(chartClick, 500);
    });

    // -------------------------------------------------------------------------
    // Filter Select Multiple with checkboxes widget.
    // -------------------------------------------------------------------------
    //
    // By default all checkbox choices are hidden, except they are selected.
    // A click on the corresponding `Show all` link displays them all.
    $('.filter-form .select-multiple').each(function(){
        var $sel = $(this);

        $sel.find('span.show-all').show();
        $sel.find('.select-all').hide();
        $sel.find('.hide-unselected').hide();

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
            $(this).parent().find('.hide-unselected').show();
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
            console.log('here');
        });

        // Collapse button
        $('.select-multiple-header span.hide-unselected', $sel).click(function(){
            $sel.find('input[type=checkbox]:not(:checked)').each(function(){
                $(this).closest('li').slideUp('fast');
            });
            $(this).hide();
            $(this).parent().find('.select-all').hide();
            $('.select-multiple-header span.show-all', $sel).show();
        });
    });
});

function chartClick(){
    $('#chart-tab').trigger('click');
}
