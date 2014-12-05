from .common import *

PROJECT_ENV='Prod'

DEBUG = False
TEMPLATE_DEBUG = DEBUG
THUMBNAIL_DEBUG = DEBUG
COMPRESS_ENABLED = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'safebee',
        'USER': 'safebee',
        'PASSWORD': 'mVeJPTirHeT9sxx*7m',
        'HOST': 'safebeeprod1.cl21xbcn12v2.us-east-1.rds.amazonaws.com',
    },
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
        'LOCATION': [
            '127.0.0.1:11211',
        ],
    },
}

INSTALLED_APPS += (
    'kombu.transport.django',
)

ALLOWED_HOSTS = ['*']

# Cache override
CACHE_CONTROL_MAX_AGE = 0

# django-storages
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
STATICFILES_STORAGE = 'loop.storage.S3StaticStorage'
THUMBNAIL_DEFAULT_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_STORAGE_BUCKET_NAME = 'media.dev.safebee.com'
AWS_STATIC_BUCKET_NAME = 'static.dev.safebee.com'
AWS_HEADERS = {
    'Expires': 'Fri, 31 Dec 2031 23:59:59 GMT',
    'Cache-Control': 'max-age=86400',
}
AWS_IS_GZIPPED = True

# S3-only keys
AWS_ACCESS_KEY_ID = "AKIAIS6QKO33FI26PXWA"
AWS_SECRET_ACCESS_KEY = "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"

AWS_S3_SECURE_URLS = False
AWS_S3_CUSTOM_DOMAIN = AWS_STORAGE_BUCKET_NAME
AWS_STATIC_CUSTOM_DOMAIN = AWS_STATIC_BUCKET_NAME
STATIC_URL = 'http://%s/' % AWS_STATIC_BUCKET_NAME
MEDIA_URL = 'http://%s/' % AWS_STORAGE_BUCKET_NAME

# Social Settings
TWITTER_API_KEY = ''
TWITTER_API_SECRET_KEY = ''
TWITTER_OAUTH_ACCESS_TOKEN = ''
TWITTER_OAUTH_SECRET_TOKEN = ''
BITLY_CUSTOM_DOMAIN = ''

# Celery
BROKER_URL = 'django://'
CELERY_ALWAYS_EAGER = True

# Disqus
DISQUS_API_KEY = 'dvy5i3y9WLVk6tspOODnATH1msUUJ5To94H2JmKiWWvMMUfMOlau58S2Zo9sOpZ9'
DISQUS_API_SECRET = 'suWyloJERGxzIwAzHutfey5j80ph0G5oUKqEyBFeBmE1vX9RsY0bz3qw78WKAg5L'
DISQUS_FORUM_SHORTNAME = 'safebee'

# SharedCount API
SHAREDCOUNT_ENABLED = False
