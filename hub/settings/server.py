"""
Example settings for local development

Use this file as a base for your local development settings and copy
it to hub/settings/local.py. It should not be checked into
your code repository.
"""
from .base import *   # pylint: disable=W0614,W0401
import os

ALLOWED_HOSTS = ('*',)

SECRET_KEY = os.environ.get('SECRET_KEY', None)

DEBUG = os.environ.get('DEBUG', False)  # Set env var to 1

ADMINS = (
    ('Benjamin Stookey', 'ben@aashe.org'),
    ('Martin Mahner', 'martin@lincolnloop.com')
)
MANAGERS = ADMINS

import dj_database_url
DATABASES = {
    'default': dj_database_url.config(),  # uses DATABASE_URL
    # 'iss': dj_database_url.config(os.environ.get('ISS_DB_URL')),
}

# aasheauth
AASHE_DRUPAL_URI = os.environ['AASHE_DRUPAL_URI']
AASHE_DRUPAL_KEY = os.environ['AASHE_DRUPAL_KEY']
AASHE_DRUPAL_KEY_DOMAIN = os.environ['AASHE_DRUPAL_KEY_DOMAIN']
AASHE_DRUPAL_COOKIE_SESSION = os.environ['AASHE_DRUPAL_COOKIE_SESSION']
AASHE_DRUPAL_COOKIE_DOMAIN = os.environ['AASHE_DRUPAL_COOKIE_DOMAIN']

# Enable debug logging
# LOGGING['loggers']['hub']['level'] = 'DEBUG'
# LOGGING['loggers']['django']['level'] = 'DEBUG'

# Very custom url and wsgi settings
# ROOT_URLCONF = 'hub.urls.local'
# WSGI_APPLICATION = 'hub.wsgi.local.application'
