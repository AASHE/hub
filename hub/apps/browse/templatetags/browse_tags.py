from __future__ import unicode_literals

from logging import getLogger

from django.forms import widgets
from django.template import Library
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string

from ....permissions import get_aashe_member_flag

logger = getLogger(__name__)
register = Library()


@register.simple_tag
def permission_flag(obj, user, icon_only=False):
    """
    Renders a HTML field using a custom template for each possible type of
    fields we support, or Bootstrap supports.
    """
    if icon_only:
        label = '''<i
            class="icon-sm icon-warning fa fa-lock"
            data-toggle="tooltip"
            data-placement="top"
            title="{label}"></i>'''
    else:
        label = '''<span class="label label-warning">
        <i class="fa fa-lock"></i> {label}</span>''''

    # Open Document has no flag
    if obj.permission == obj.PERMISSION_CHOICES.open:
        return ''

    # If the user is logged in, and the member permission is met,
    # all fine, no label.
    if user.is_authenticated():
        is_member = get_aashe_member_flag(user)
        if (obj.permission == obj.PERMISSION_CHOICES.member and not is_member):
            return mark_safe(label.format(label='Membership Required'))
        else:
            return ''

    # We know the user is not logged in, so give a proper label, either
    # member or just login required.
    if obj.permission == obj.PERMISSION_CHOICES.member:
        return mark_safe(label.format(label='Membership Required'))

    return mark_safe(label.format(label='Login Required'))


# <widget>: <template name to render>
FIELD_MAP = {
    widgets.HiddenInput: 'hidden',
    widgets.CheckboxInput: 'checkbox',
    widgets.CheckboxSelectMultiple: 'checkbox_multiple',
    widgets.Select: 'select',
    widgets.SelectMultiple: 'select_multiple',
    widgets.RadioSelect: 'checkbox_multiple',
    widgets.Textarea: 'textarea',
}


@register.simple_tag
def render_form(form, field=None, type='input'):
    """
    Renders a Django form, field by field, while rendering each field with a
    special template according to it's widget.

    We need to do that since the HTML layout of a Bootstrap field differs
    heavily per type.
    """
    response = ''

    if field:  # Just this specific field
        rendered_field_list = [f for f in form.__iter__() if f.name == field]
    else:  # Or all fields
        rendered_field_list = form.__iter__()

    # Iterate over all fields and render each one with the matching template
    for f in rendered_field_list:
        widget = f.field.widget.__class__
        field_type = FIELD_MAP.get(widget, 'input')
        template_name = 'forms/{}.html'.format(field_type)
        response += render_to_string(template_name, {'field': f})

    return mark_safe(response)
