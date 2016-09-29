from django_filters.widgets import LinkWidget
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
from django.db.models.fields import BLANK_CHOICE_DASH


class GalleryViewWidget(LinkWidget):
    """
    Custom LinkWidget for the gallery view
    """

    def __init__(self, attrs=None, choices=(), initial=None):
        super(GalleryViewWidget, self).__init__(attrs)
        self.initial = initial

    def render(self, name, value, attrs=None, choices=()):
        if not value and self.initial:
            value = self.initial

        safe_output = super(GalleryViewWidget, self).render(
            name, value, attrs, choices)

        # append the hidden input so that this value persists
        dom_str = '\n<input name="%s" type="hidden" value="%s">'
        return safe_output + dom_str % (name, value)

    def render_option(self, name, selected_choices,
                      option_value, option_label):
        option_value = force_text(option_value)
        if option_label == BLANK_CHOICE_DASH[0][1]:
            option_label = _("All")
        data = self.data.copy()
        data[name] = option_value
        selected = data == self.data or option_value in selected_choices
        try:
            url = data.urlencode()
        except AttributeError:
            url = urlencode(data)
        return self.option_string() % {
            'attrs': selected and ' class="selected"' or '',
            'query_string': url,
            'icon': "picture-o" if option_value == "gallery" else "list",
            'help_text':
                "Gallery View" if option_value == "gallery" else "List View"
        }

    def option_string(self):
        return '''
            <li%(attrs)s>
                <a
                    class="btn btn-default"
                    href="?%(query_string)s"
                    title="%(help_text)s">
                <i class="fa fa-%(icon)s pull-right"></i></a>
            </li>'''
