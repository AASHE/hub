"""
Settings specifically for a dev server.

Pulls ADMIN info from environment and adds django-extensions and
django-debug-toolbar to INSTALLED_APPS.
"""
from .server import *   # pyflakes: disable=F403  # NOQA

ADMINS = (
    (os.environ.get('ADMIN_NAME', 'AASHE IT'),
     os.environ.get('ADMIN_EMAIL', 'it@aashe.org')),
)
MANAGERS = ADMINS

INSTALLED_APPS += ('django_extensions',)

DEBUG_TOOLBAR = os.environ.get('DEBUG_TOOLBAR', False)
if DEBUG_TOOLBAR:
    INSTALLED_APPS = INSTALLED_APPS + ('debug_toolbar',)
