/*

    Submit Form Javascript

*/
jQuery(document).ready(function() {
    // -------------------------------------------------------------------------
    // Add a datepicker to everything which looks like a datefield
    // -------------------------------------------------------------------------
    $('input[name*=date]').each(function() {
        new Pikaday({
            field: $(this)[0],
            format: 'YYYY-MM-DD'
         });
    });

    // -------------------------------------------------------------------------
    // Other large dropdowns
    // -------------------------------------------------------------------------
    $('select[name*=topics], select[name*=disciplines], select[name*=institutions]').selectize();

    // -------------------------------------------------------------------------
    // Keywords (like tags)
    // -------------------------------------------------------------------------
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
