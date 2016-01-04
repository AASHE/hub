"""Base settings shared by all environments"""

# Import global settings to make it easier to extend settings.
from django.conf.global_settings import *   # pylint: disable=W0614,W0401

#==============================================================================
# Generic Django project settings
#==============================================================================

WSGI_APPLICATION = 'hub.wsgi.application'

DEBUG = False

SITE_ID = 1

TIME_ZONE = 'UTC'
USE_TZ = True
USE_I18N = False
USE_L10N = False
LANGUAGE_CODE = 'en'
LANGUAGES = (
    ('en', 'English'),
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'aashe.aasheauth.backends.AASHEBackend',
)

AUTH_USER_MODEL = 'auth.User'

INSTALLED_APPS = (
    'flat',

    'aashe.aasheauth',
    'block_content',
    'haystack',
    'iss',
    'sorl.thumbnail',
    'typogrify',

    'hub',
    'hub.apps.content',
    'hub.apps.metadata',
    'hub.apps.browse',
    'hub.apps.submit',

    'django_tables2',
    'django_markup',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [],
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
        ],
    }
}]

# ==============================================================================
# Calculation of directories relative to the project module location
# ==============================================================================

import os
import sys
import hub as project_module

PROJECT_DIR = os.path.dirname(os.path.realpath(project_module.__file__))

PYTHON_BIN = os.path.dirname(sys.executable)
ve_path = os.path.dirname(os.path.dirname(os.path.dirname(PROJECT_DIR)))
# Assume that the presence of 'activate_this.py' in the python bin/
# directory means that we're running in a virtual environment.
if os.path.exists(os.path.join(PYTHON_BIN, 'activate_this.py')):
    # We're running with a virtualenv python executable.
    VAR_ROOT = os.path.join(os.path.dirname(PYTHON_BIN), 'var')
elif ve_path and os.path.exists(os.path.join(ve_path, 'bin',
        'activate_this.py')):
    # We're running in [virtualenv_root]/src/[project_name].
    VAR_ROOT = os.path.join(ve_path, 'var')
else:
    # Set the variable root to a path in the project which is
    # ignored by the repository.
    VAR_ROOT = os.path.join(PROJECT_DIR, 'var')

if not os.path.exists(VAR_ROOT):
    os.mkdir(VAR_ROOT)

# ==============================================================================
# Project URLS and media settings
# ==============================================================================

ROOT_URLCONF = 'hub.urls'

LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'
LOGIN_REDIRECT_URL = '/'

STATICFILES_DIRS = (
    os.path.join(PROJECT_DIR, 'static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

STATIC_URL = '/static/'
MEDIA_URL = '/uploads/'

STATIC_ROOT = os.path.join(VAR_ROOT, 'static')
MEDIA_ROOT = os.path.join(VAR_ROOT, 'uploads')

# ==============================================================================
# Email
# ==============================================================================

EMAIL_BACKEND = os.environ.get(
    'EMAIL_BACKEND', 'django.core.mail.backends.filebased.EmailBackend')
EMAIL_FILE_PATH = os.environ.get(
    'EMAIL_FILE_PATH', '/tmp/hub-email-messages')
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', True)
EMAIL_HOST = os.environ.get('EMAIL_HOST', None)
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', None)
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', None)
EMAIL_PORT = os.environ.get('EMAIL_PORT', None)
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', None)
EMAIL_REPLY_TO = os.environ.get('EMAIL_REPLY_TO', None)

# ==============================================================================
# Miscellaneous project settings
# ==============================================================================

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'formatters': {
        'verbose': {
            'format': (
                '%(asctime)s [%(process)d] [%(levelname)s] ' +
                'pathname=%(pathname)s lineno=%(lineno)s ' +
                'funcname=%(funcName)s %(message)s'
            ),
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },

        'simple': {
            'format': '%(levelname)s %(message)s',
        },
    },

    'loggers': {
        'django': {
            'level': 'ERROR',
            'handlers': ['console'],
        },
        'hub': {
            'level': 'ERROR',
            'handlers': ['console'],
        },
    },
}

# ==============================================================================
# Third party app settings
# ==============================================================================

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://127.0.0.1:9200/',
        'INDEX_NAME': 'haystack',
    },
}

# Cache lifetime in seconds
CACHE_TTL_SHORT = 60 * 10
CACHE_TTL_LONG = 60 * 60 * 12

# AASHE Auth
AASHE_DRUPAL_URI = os.environ['AASHE_DRUPAL_URI']
AASHE_DRUPAL_KEY = os.environ['AASHE_DRUPAL_KEY']
AASHE_DRUPAL_KEY_DOMAIN = os.environ['AASHE_DRUPAL_KEY_DOMAIN']
AASHE_DRUPAL_COOKIE_SESSION = os.environ['AASHE_DRUPAL_COOKIE_SESSION']
AASHE_DRUPAL_COOKIE_DOMAIN = os.environ['AASHE_DRUPAL_COOKIE_DOMAIN']

# List of content type keys which don't require Login This only enables the
# 'browse' view of the content type. Each object must still be separately set to
# `member_only=False` to make it open.
PUBLIC_CONTENT_TYPES = (
    'academicprogram',
)
