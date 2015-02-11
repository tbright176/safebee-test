from .common import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG
COMPRESS_ENABLED = False
THUMBNAIL_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'safebee_db',
        'USER': 'vagrant',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

INSTALLED_APPS += (
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


AWS_ACCESS_KEY_ID = "AKIAIS6QKO33FI26PXWA"
AWS_SECRET_ACCESS_KEY = "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"
SNS_TOPIC_RECALL_NEWSLETTER = 'Safebee-Recalls-TEST'
