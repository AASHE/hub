from __future__ import unicode_literals

from logging import getLogger

from django.template import Library
from django.utils.safestring import mark_safe

logger = getLogger(__name__)
register = Library()


@register.simple_tag
def permission_flag(obj, user):
    """
    Renders a HTML field using a custom template for each possible type of
    fields we support, or Bootstrap supports. At this point we don't really know
    which type of widget the field were, so we guess it based on the original
    HTML output.
    """
    label = '<span class="label label-warning"><i class="fa fa-lock"></i> {label}</span>'
    flag = obj.permission_flag(user)
    if flag == 'login-required':
        return mark_safe(label.format(label='Login Required'))
    if flag == 'member-required':
        return mark_safe(label.format(label='Membership Required'))
    return ''
