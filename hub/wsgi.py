"""
WSGI config for hub project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Use the local settings file if one is present, otherwise the server.
try:
    import hub.settings.local
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hub.settings.local")
except ImportError:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hub.settings.server")

application = get_wsgi_application()
