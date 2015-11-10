from .common import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG
COMPRESS_ENABLED = False
THUMBNAIL_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'safebee_db',
        'USER': 'safebee',
        'HOST': 'localhost',
        'PASSWORD': 'changeme',
    },
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

INSTALLED_APPS += (
    'debug_toolbar.apps.DebugToolbarConfig',
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

AWS_ACCESS_KEY_ID = "AKIAIS6QKO33FI26PXWA"
AWS_SECRET_ACCESS_KEY = "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"
SNS_TOPIC_RECALL_NEWSLETTER = 'Safebee-Recalls-TEST'

# django-storages
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
THUMBNAIL_DEFAULT_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_STORAGE_BUCKET_NAME = 'media.test.safebee.com'
AWS_HEADERS = {
    'Expires': 'Fri, 31 Dec 2031 23:59:59 GMT',
    'Cache-Control': 'max-age=2592000',
}
AWS_IS_GZIPPED = True

# S3-only keys
AWS_ACCESS_KEY_ID = "AKIAIS6QKO33FI26PXWA"
AWS_SECRET_ACCESS_KEY = "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"
AWS_QUERYSTRING_AUTH = False
AWS_S3_SECURE_URLS = False
MEDIA_URL = 'https://s3.amazonaws.com/{}/'.format(AWS_STORAGE_BUCKET_NAME)
