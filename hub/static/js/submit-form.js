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
    $('select[name*=topics], select[name*=disciplines], select[name*=institutions]').selectize({
        maxItems: 3,
        plugins: ['required-options',],
        required_values: []
    });

    if(preset_topics != undefined) {
        $('select[name*=topics]')[0].selectize.settings.required_values = preset_topics
    }
    
    // -------------------------------------------------------------------------
    // Tagging (Keywords)
    // -------------------------------------------------------------------------
    updateTagSubmitDropdowns();

    // -------------------------------------------------------------------------
    // Initialize the in-line form buttons
    // -------------------------------------------------------------------------
    $('#add-author').djangoInlineFormAdd({
      prefix: "author",
      postClick: updateOrgDropdowns,
      formHeight: 200,
    });
    $('#i-am-author').djangoInlineFormAdd({
      prefix: 'author',
      templateId: '#author-template-user-is-author',
      postClick: updateOrgDropdowns,
      formHeight: 200
    });
    $('#add-file').djangoInlineFormAdd({
      prefix: "file",
      formHeight: 300,
    });
    $('#add-image').djangoInlineFormAdd({
      prefix: "image",
      formHeight: 300,
    });
    $('#add-website').djangoInlineFormAdd({
      prefix: "website",
      formHeight: 150,
    });
});
