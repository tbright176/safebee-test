from .common import *


DEBUG = True
TEMPLATE_DEBUG = True
COMPRESS_ENABLED = False
THUMBNAIL_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'safebee',
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
    'debug_toolbar.apps.DebugToolbarConfig',
    'django_extensions',
    'devserver',
    'kombu.transport.django',
)

ALLOWED_HOSTS = ['*', 'localhost', '127.0.0.1',]

DEVSERVER_MODULES = (
    'devserver.modules.sql.SQLRealTimeModule',
    'devserver.modules.sql.SQLSummaryModule',
    'devserver.modules.profile.ProfileSummaryModule',

    # Modules not enabled by default
    'devserver.modules.ajax.AjaxDumpModule',
    'devserver.modules.profile.MemoryUseModule',
    'devserver.modules.cache.CacheSummaryModule',
    'devserver.modules.profile.LineProfilerModule',
)

# Cache override
CACHE_CONTROL_MAX_AGE = 0

# django-storages
#DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
#STATICFILES_STORAGE = 'loop.storage.S3StaticStorage'
#THUMBNAIL_DEFAULT_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
#AWS_STORAGE_BUCKET_NAME = 'media.dev.safebee.com'
#AWS_STATIC_BUCKET_NAME = 'static.dev.safebee.com'
#AWS_HEADERS = {
#    'Expires': 'Fri, 31 Dec 2031 23:59:59 GMT',
#    'Cache-Control': 'max-age=86400',
#}
#AWS_IS_GZIPPED = True

# S3-only keys
AWS_ACCESS_KEY_ID = "AKIAIS6QKO33FI26PXWA"
AWS_SECRET_ACCESS_KEY = "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"

#AWS_S3_SECURE_URLS = False
#AWS_S3_CUSTOM_DOMAIN = AWS_STORAGE_BUCKET_NAME
#AWS_STATIC_CUSTOM_DOMAIN = AWS_STATIC_BUCKET_NAME
#STATIC_URL = 'http://%s/' % AWS_STATIC_BUCKET_NAME
#MEDIA_URL = 'http://%s/' % AWS_STORAGE_BUCKET_NAME


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
DISQUS_API_KEY = 'BM9Wn7cGlRFHorecicATYQ56BDSYrl8puaOHSwQUWsPKhe445NUOcJ9Ur9uqSYy8'
DISQUS_API_SECRET = 'SzgyXMXqvUVMmUJwKp5yu7PNNAdoMTrHpvvPcpAMxklMJkOM8Q2V9zOFtvKqzIWs'
DISQUS_FORUM_SHORTNAME = 'safebee-dev'
SNS_TOPIC_RECALL_NEWSLETTER = 'Safebee-Recalls-TEST'
