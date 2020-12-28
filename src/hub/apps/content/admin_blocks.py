import django_admin_blocks
from linkcheck.models import Link
from django.core.urlresolvers import reverse


def linkcheck_app_block():
    return "<a href='%s'>Link Checker</a>" % reverse('linkchecker')


django_admin_blocks.register({
    'script_blocks': [
        {'url_path': 'js/admin_sortable/jquery-ui-1.10.3.custom.min.js'},
        {'url_path': 'js/admin_sortable/admin_sortable.js'},
    ],
})
