from logging import getLogger

from django.template.loader import render_to_string
from django.template import Library
from django.utils.safestring import mark_safe

logger = getLogger(__name__)
register = Library()

# <str to search>: <template name to render>
FIELD_MAP = {
    '<li>': 'checkbox-multiple',
    'id_order': 'checkbox-multiple',
    'type="checkbox"': 'checkbox',
    'type="radio"': 'checkbox-multiple',
    '<select multiple="multiple"': 'select_multiple',
    '<select': 'select',
    '<textarea': 'textarea',
}


@register.simple_tag
def render_field(field, type='input'):
    """
    Renders a HTML field using a custom template for each possible type of
    fields we support, or Bootstrap supports. At this point we don't really know
    which type of widget the field were, so we guess it based on the original
    HTML output.
    """
    field_type = 'input'
    for k, v in FIELD_MAP.items():
        if k in field.__str__():
            field_type = v
    template_name = 'submit/forms/{}.html'.format(field_type)
    return mark_safe(render_to_string(template_name, {'field': field}))
