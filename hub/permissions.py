from __future__ import unicode_literals

from logging import getLogger

from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.db.models import ObjectDoesNotExist

from hub.apps.access.models import TemporaryUser
from datetime import date

logger = getLogger(__name__)


class LoginRequiredMixin(object):
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated():
            return render(
                self.request, 'registration/login_required.html',
                status=HttpResponseForbidden.status_code)
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


def get_aashe_member_flag(user):
    """
    Tries to get the AASHE member flag of a given user object.
    Returns also True in case the user object is a superuser.
    """
    # Superusers are super users
    if user.is_superuser:
        return True

    if user.is_authenticated():
        temp_user_set = TemporaryUser.objects.filter(
            email_address=user.email,
            access_starts__lte=date.today(),
            access_ends__gte=date.today()
            )
        if temp_user_set:
            return True

    # Try to determine the actual AASHE member flag. This can fail for two
    # reasons, actually just one: The user object is a standard contrib.user
    # object, likely created with `manage.py createsuperuser` and therefor
    # has no AASHE user account attached.
    try:
        return user.membersuiteportaluser.is_member
    except (ObjectDoesNotExist, AttributeError):
        return False

    return False
