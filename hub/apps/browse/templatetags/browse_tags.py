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
        <i class="fa fa-lock"></i> {label}</span>'''

    # Open Document has no flag
    if obj.permission == obj.PERMISSION_CHOICES.open:
        return ''

    # If the user is logged in, and the member permission is met,
    # all fine, no label.
    if user.is_authenticated():
        is_member = get_aashe_member_flag(user)
        if (obj.permission == obj.PERMISSION_CHOICES.member and not is_member):
            return mark_safe(label.format(label='The information page about'
                                          ' this resource is accessible only to AASHE'
                                          ' members.'))
        else:
            return ''

    # We know the user is not logged in, so give a proper label, either
    # member or just login required.
    if obj.permission == obj.PERMISSION_CHOICES.member:
        return mark_safe(label.format(label='The information page about this'
                                      ' resource is accessible only to AASHE members.'))

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


@register.simple_tag
def video_embed(link):
    """
        Prep vimeo and youtube links for embedded videos
    """
    if "vimeo" in link:
        begin = "https://player.vimeo.com/video/"
        end = link.rpartition('/')[2]
    elif "youtu" in link:
        begin = "https://www.youtube.com/embed/"
        end = link.rpartition('/')[2]
        if "watch" in link:
            video_marker = "v="
            start_position = link.find(video_marker)+len(video_marker)
            end = link[start_position:start_position + 11]
    else:
        hidden_return = "<div style='display:none;'></div>"
        return mark_safe(hidden_return)

    full_return = "<div style='margin-bottom:13px;\
        'class='embed-responsive embed-responsive-16by9'>\
        <iframe src='" + begin + end + "'></iframe></div>"

    return mark_safe(full_return)


@register.simple_tag
def mask_url(link):
    """
    Mask url of uploaded file, so it does not show that it is from S3
    """
    begin = "https://hub-media.aashe.org/uploads/"
    if "amazonaws.com" in link:
        end = link.rpartition('/')[2]
        return (begin + end).replace("+", "%2B")
    return link.replace("+", "%2B")
