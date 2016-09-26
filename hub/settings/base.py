"""Base settings shared by all environments"""
import os
import sys

# Import global settings to make it easier to extend settings.
from django.conf.global_settings import *   # pylint: disable=W0614,W0401  # NOQA

import hub as project_module


PROJECT_DIR = os.path.dirname(os.path.realpath(project_module.__file__))

PYTHON_BIN = os.path.dirname(sys.executable)

# =============================================================================
# Generic Django project settings
# =============================================================================
WSGI_APPLICATION = 'hub.wsgi.application'

DEBUG = os.environ.get('DEBUG', False)
THUMBNAIL_DEBUG = DEBUG

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
    'aashe_theme',
    'block_content',
    'haystack',
    'iss',
    'import_export',
    'sorl.thumbnail',
    'tagulous',
    'typogrify',
    'integration_settings.google_analytics',
    's3direct',
    'bootstrap_pagination',
    'linkcheck',
    'django_admin_blocks',

    'hub',
    'hub.apps.access',
    'hub.apps.content',
    'hub.apps.metadata',
    'hub.apps.browse',
    'hub.apps.submit',
    'hub.exports',

    'acme_challenge',
    'django_tables2',
    'django_markup',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.flatpages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django_password_protect.PasswordProtectMiddleware',
    'hub.middleware.HerokuRemoteAddr',
    'sslify.middleware.SSLifyMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
)

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [os.path.join(PROJECT_DIR, 'templates'), ],
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
            'django.core.context_processors.request',
            'hub.apps.browse.context_processors.cache_vars',
        ],
        'debug': DEBUG,
    }
}]

# ==============================================================================
# Calculation of directories relative to the project module location
# ==============================================================================

ve_path = os.path.dirname(os.path.dirname(os.path.dirname(PROJECT_DIR)))
# Assume that the presence of 'activate_this.py' in the python bin/
# directory means that we're running in a virtual environment.
if os.path.exists(os.path.join(PYTHON_BIN, 'activate_this.py')):
    # We're running with a virtualenv python executable.
    VAR_ROOT = os.path.join(os.path.dirname(PYTHON_BIN), 'var')
elif ve_path and os.path.exists(os.path.join(
        ve_path, 'bin', 'activate_this.py')):
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
    # 'compressor.finders.CompressorFinder',
)

STATIC_URL = '/static/'
MEDIA_URL = '/uploads/'

STATIC_ROOT = os.path.join(VAR_ROOT, 'static')
MEDIA_ROOT = os.path.join(VAR_ROOT, 'uploads')

# COMPRESS_ENABLED = os.environ.get('COMPRESS_ENABLED', True)
# COMPRESS_CSS_FILTERS = [
#     # 'compressor.filters.cssmin.rCSSMinFilter',
#     # 'compressor.filters.cleancss.CleanCSSFilter',
# ]

TAGULOUS_AUTOCOMPLETE_JS = None

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

eng = 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine'
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': eng,
        'URL': 'http://127.0.0.1:9200/',
        'INDEX_NAME': 'haystack',
        'TIMEOUT': 30
    },
}

# Debug Toolbar
DEBUG_TOOLBAR = os.environ.get('DEBUG_TOOLBAR', False)
if DEBUG_TOOLBAR:
    INSTALLED_APPS += ('debug_toolbar',)

# Cache lifetime in seconds
CACHE_TTL_SHORT = 60 * 10  # 10 minutes
CACHE_TTL_LONG = 60 * 60 * 12  # 12 hours

import django_cache_url
CACHE_URL = os.environ.get('CACHE_URL', 'dummy://')
CACHES = {'default': django_cache_url.parse(CACHE_URL)}

# AASHE Auth
AASHE_DRUPAL_URI = os.environ['AASHE_DRUPAL_URI']
AASHE_DRUPAL_KEY = os.environ['AASHE_DRUPAL_KEY']
AASHE_DRUPAL_KEY_DOMAIN = os.environ['AASHE_DRUPAL_KEY_DOMAIN']
AASHE_DRUPAL_COOKIE_SESSION = os.environ['AASHE_DRUPAL_COOKIE_SESSION']
AASHE_DRUPAL_COOKIE_DOMAIN = os.environ['AASHE_DRUPAL_COOKIE_DOMAIN']

# List of content type keys which don't require Login This only enables the
# 'browse' view of the content type. Each object must still be separately set
# to `member_only=False` to make it open.
PUBLIC_CONTENT_TYPES = (
    'academicprogram',
)

GOOGLE_ANALYTICS_PROPERTY_ID = os.environ.get(
    'GOOGLE_ANALYTICS_PROPERTY_ID', None)

# django-acme-challenge for Let's Encrypt
ACME_CHALLENGE_URL_SLUG = os.environ.get('ACME_CHALLENGE_URL_SLUG', None)
ACME_CHALLENGE_TEMPLATE_CONTENT = os.environ.get(
    'ACME_CHALLENGE_TEMPLATE_CONTENT', None)

# Optional password protection for dev sites
PASSWORD_PROTECT = os.environ.get('PASSWORD_PROTECT', False)
PASSWORD_PROTECT_USERNAME = os.environ.get('PASSWORD_PROTECT_USERNAME', None)
PASSWORD_PROTECT_PASSWORD = os.environ.get('PASSWORD_PROTECT_PASSWORD', None)
PASSWORD_PROTECT_REALM = os.environ.get(
    'PASSWORD_PROTECT_REALM', 'Dev Site Auth')

# Rate Limiting
# Using these so we can limit to speed up testing - change in production
RATELIMIT_ENABLE = os.environ.get('RATELIMIT_ENABLE', False)
LOGIN_RATE_LIMIT = os.environ.get('LOGIN_RATE_LIMIT', '5/5m')
BROWSE_RATE_LIMIT = os.environ.get('BROWSE_RATE_LIMIT', '5/5m')
API_RATE_LIMIT = os.environ.get('API_RATE_LIMIT', '5/5m')

ALLOWED_FILE_TYPES = [
    'text/csv',
    'application/pdf',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.template',
    'application/vnd.ms-excel',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.template',
    'application/vnd.ms-powerpoint',
    'application/vnd.openxmlformats-officedocument.presentationml.presentation',
    'application/vnd.openxmlformats-officedocument.presentationml.template',
    'application/vnd.openxmlformats-officedocument.presentationml.slideshow',
]

S3DIRECT_REGION = os.environ.get('S3DIRECT_REGION', 'us-east-1')
S3DIRECT_DESTINATIONS = {
    # Limit uploads to jpeg's and png's.
    'images': {
        'key': 'uploads',
        'auth': lambda u: u.is_authenticated(),
        'allowed': ['image/jpeg', 'image/png'],
    },
    # Limit uploads to PDF, Excel, Word, PPT
    # we could consider adding more: http://bit.ly/29HjwO2
    'files': {
        'key': 'uploads',
        'auth': lambda u: u.is_authenticated(),
        'allowed': ALLOWED_FILE_TYPES,
    },
}

# ==============================================================================
# Link checking
# ==============================================================================
LINKCHECK_EXTERNAL_RECHECK_INTERVAL = os.environ.get(
    'LINKCHECK_EXTERNAL_RECHECK_INTERVAL', 10080)
LINKCHECK_EXTERNAL_REGEX_STRING = os.environ.get(
    'LINKCHECK_EXTERNAL_REGEX_STRING', r'^https?://')
LINKCHECK_MEDIA_PREFIX = os.environ.get('LINKCHECK_MEDIA_PREFIX', '/media/')
LINKCHECK_RESULTS_PER_PAGE = os.environ.get('LINKCHECK_RESULTS_PER_PAGE', 25)
LINKCHECK_MAX_URL_LENGTH = os.environ.get('LINKCHECK_MAX_URL_LENGTH', 255)
LINKCHECK_CONNECTION_ATTEMPT_TIMEOUT = os.environ.get(
    'LINKCHECK_CONNECTION_ATTEMPT_TIMEOUT', 10)
SITE_DOMAIN = os.environ.get('SITE_DOMAIN', 'testserver')

# ==============================================================================
# Celery
# ==============================================================================

# in dev mode, celery won't use redis or a background task, but work inline
# set the env var to 1 or 0 (or don't set it at all)
# Since Heroku can set the broker URL, we have to create the intermediate
# variable `CELERY_BROKER_VAR` to be flexible
CELERY_ALWAYS_EAGER = os.environ.get('CELERY_ALWAYS_EAGER', '1') == '1'
CELERY_BROKER_VAR = os.environ.get('CELERY_BROKER_VAR', '')
BROKER_URL = os.environ.get(CELERY_BROKER_VAR, None)
CELERY_ACCEPT_CONTENT = ['json', ]
CELERY_TASK_SERIALIZER = 'json'
# No backend needed right now, since we're not storing results
# CELERY_RESULT_BACKEND = os.environ.get('CELERY_BACKEND_URL', None)

GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY', None)
