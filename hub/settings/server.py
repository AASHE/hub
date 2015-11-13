"""
HEROKU specific settings
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

# Database
import dj_database_url
DATABASES = {
    'default': dj_database_url.config(),  # uses DATABASE_URL
    # 'iss': dj_database_url.config(os.environ.get('ISS_DB_URL')),
}

# Haystack ElasticSearch
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': os.environ.get('SEARCHBOX_SSL_URL', None),
        'INDEX_NAME': 'haystack',
    },
}

# ==============================================================================
# aasheauth
# ==============================================================================
AASHE_DRUPAL_URI = os.environ['AASHE_DRUPAL_URI']
AASHE_DRUPAL_KEY = os.environ['AASHE_DRUPAL_KEY']
AASHE_DRUPAL_KEY_DOMAIN = os.environ['AASHE_DRUPAL_KEY_DOMAIN']
AASHE_DRUPAL_COOKIE_SESSION = os.environ['AASHE_DRUPAL_COOKIE_SESSION']
AASHE_DRUPAL_COOKIE_DOMAIN = os.environ['AASHE_DRUPAL_COOKIE_DOMAIN']

# ==============================================================================
# iss
# ==============================================================================
SALESFORCE_USERNAME = os.environ.get('SALESFORCE_USERNAME', None)
SALESFORCE_PASSWORD = os.environ.get('SALESFORCE_PASSWORD', None)
SALESFORCE_SECURITY_TOKEN = os.environ.get('SALESFORCE_SECURITY_TOKEN', None)

# ==============================================================================
# S3 Media Storage
# ==============================================================================
INSTALLED_APPS += ('s3_folder_storage',)

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", None)
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", None)
AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME", None)

# User uploaded media
DEFAULT_FILE_STORAGE = 's3_folder_storage.s3.DefaultStorage'
DEFAULT_S3_PATH = "uploads"
MEDIA_ROOT = '/%s/' % DEFAULT_S3_PATH
MEDIA_URL = '//s3.amazonaws.com/%s/uploads/' % AWS_STORAGE_BUCKET_NAME

# Static files, Using whitenoise now
##STATICFILES_STORAGE = 's3_folder_storage.s3.StaticStorage'
##STATIC_S3_PATH = "static"
##STATIC_ROOT = "/%s/" % STATIC_S3_PATH
##STATIC_URL = '//s3.amazonaws.com/%s/static/' % AWS_STORAGE_BUCKET_NAME
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

# ==============================================================================
# Enable debug logging
# ==============================================================================
# LOGGING['loggers']['hub']['level'] = 'DEBUG'
# LOGGING['loggers']['django']['level'] = 'DEBUG'

# Very custom url and wsgi settings
# ROOT_URLCONF = 'hub.urls.local'
# WSGI_APPLICATION = 'hub.wsgi.local.application'
