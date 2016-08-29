"""
WSGI config for hub project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os

# Use the local settings file if one is present, otherwise the server.
try:
    import hub.settings.local
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hub.settings.local")
except ImportError:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hub.settings.server")


from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise

application = get_wsgi_application()
application = DjangoWhiteNoise(application)
