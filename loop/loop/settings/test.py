from .common import *

import dj_database_url

DEBUG = True
THUMBNAIL_DEBUG = False

DATABASES = {}

for key in os.environ.keys():
    if key.startswith('DJANGO_DB_'):
        try:
            label = key.split('_')[2]
        except IndexError:
            continue

        DATABASES[label.lower()] = dj_database_url.parse(os.environ.get(key))

DATABASES['default']['CONN_MAX_AGE'] = 600

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
        'LOCATION': '{}:11211'.format(os.environ.get('DJANGO_MEMCACHE')),
    }
}

TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)

ALLOWED_HOSTS = [
    '.mnndev.com',
    '.compute-1.amazonaws.com',
]

# Static
STATICFILES_STORAGE = 'loop.storage.S3StaticStorage'
static_bucket = os.environ.get('DJANGO_STATIC_BUCKET')
STATIC_URL = 'https://s3.amazonaws.com/{}/'.format(static_bucket)
AWS_STATIC_BUCKET_NAME = static_bucket
AWS_STATIC_CUSTOM_DOMAIN = None

COMPRESS_ENABLED = True
COMPRESS_STORAGE = 'loop.storage.S3StaticStorage'

# Django-Storages
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_STORAGE_BUCKET_NAME = 'media.dev.safebee.com'
AWS_S3_SECURE_URLS = False
AWS_QUERYSTRING_AUTH = False

MEDIA_URL = 'https://s3.amazonaws.com/{}/'.format(AWS_STORAGE_BUCKET_NAME)

# Easy Thumbnails
THUMBNAIL_DEFAULT_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
DEBUG = True
TEMPLATE_DEBUG = True
