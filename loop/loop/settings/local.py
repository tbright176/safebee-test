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
CELERY_ALWAYS_EAGER = True
