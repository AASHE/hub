Selectize.define('required-options', function(options) {
    options = $.extend({
        required_values: [],
    }, options);

    var self = this;

    this.removeItem = (function() {
        var original = self.removeItem;
        return function(value, silent) {
            if($.inArray(value, self.settings.required_values) == -1) {
                return original.apply(this, [value, silent]);
            }
        }
    })();
});
