from .common import *


DEBUG = False
TEMPLATE_DEBUG = DEBUG
THUMBNAIL_DEBUG = DEBUG
COMPRESS_ENABLED = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'loop',
        'USER': 'ftguser',
        'PASSWORD': 'UJPadM.PR92u',
        'HOST': 'fromthegrapevineprod1.cl21xbcn12v2.us-east-1.rds.amazonaws.com',
    },
}

CACHES = {
    'default': {
        'BACKEND': 'django_pylibmc.memcached.PyLibMCCache',
        'LOCATION': '',
        'TIMEOUT': 500,
        'BINARY': True,
        'OPTIONS': {  # Maps to pylibmc "behaviors"
            'tcp_nodelay': True,
            'ketama': True
        }
    }
}

INSTALLED_APPS += (

)

ALLOWED_HOSTS = ['*']

# django-storages
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
STATICFILES_STORAGE = 'loop.storage.S3StaticStorage'
THUMBNAIL_DEFAULT_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_STORAGE_BUCKET_NAME = ''
AWS_STATIC_BUCKET_NAME = ''
AWS_HEADERS = {
    'Expires': 'Fri, 31 Dec 2031 23:59:59 GMT',
    'Cache-Control': 'max-age=86400',
}
AWS_IS_GZIPPED = True

# S3-only keys
AWS_ACCESS_KEY_ID = ""
AWS_SECRET_ACCESS_KEY = ""

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
