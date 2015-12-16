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
    
    // -------------------------------------------------------------------------
    // Initialize the in-line form buttons
    // -------------------------------------------------------------------------
    $('#add-author').djangoInlineFormAdd({
      prefix: "authors",
      postClick: $.updateOrgDropdowns,
      formHeight: 200,
    });
    $('#i-am-author').djangoInlineFormAdd({
      prefix: 'authors',
      templateId: '#authors-template-user-is-author',
      postClick: $.updateOrgDropdowns,
      formHeight: 200
    });
    $('#add-file').djangoInlineFormAdd({
      prefix: "files",
      formHeight: 300,
      deleteButtonId: '#delete-file'
    });
    $('#add-image').djangoInlineFormAdd({
      prefix: "images",
      formHeight: 300,
      deleteButtonId: '#delete-image'
    });
});