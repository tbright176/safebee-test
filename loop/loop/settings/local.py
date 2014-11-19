from .common import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG
COMPRESS_ENABLED = False
THUMBNAIL_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'loop_db',
        'USER': 'vagrant',
    },
}

INSTALLED_APPS += (
    'debug_toolbar.apps.DebugToolbarConfig',
    'django_nose',
    'kombu.transport.django',
)

ALLOWED_HOSTS = ['*',]

# Django Nose Test Settings
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = [
    '--with-coverage',
    '--cover-package=core,asset_manager',
]

# Social Settings
TWITTER_API_KEY = ''
TWITTER_API_SECRET_KEY = ''
TWITTER_OAUTH_ACCESS_TOKEN = ''
TWITTER_OAUTH_SECRET_TOKEN = ''
BITLY_CUSTOM_DOMAIN = ''

# Celery
BROKER_URL = 'django://'

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'debug_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': 'error.log',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['debug_file', 'error_file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'recalls': {
            'handlers': ['console',],
            'level': 'INFO',
            'propagate': True,
        },
    },
}


AWS_ACCESS_KEY_ID = "AKIAIS6QKO33FI26PXWA"
AWS_SECRET_ACCESS_KEY = "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"
