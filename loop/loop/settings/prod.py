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
        'CONN_MAX_AGE': 600,
    },
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
        'LOCATION': 'safebee-prod.a5liiu.cfg.use1.cache.amazonaws.com:11211',
        'TIMEOUT': 600,
        'BINARY': True,
        'OPTIONS': {  # Maps to pylibmc "behaviors"
            'tcp_nodelay': True,
            'ketama': True
        }
    },
}

INSTALLED_APPS += (
    'kombu.transport.django',
)

ALLOWED_HOSTS = ['*']

# Cache override
CACHE_CONTROL_MAX_AGE = 60 * 10

# django-storages
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
STATICFILES_STORAGE = 'loop.storage.S3StaticStorage'
THUMBNAIL_DEFAULT_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_STORAGE_BUCKET_NAME = 'media.dev.safebee.com'
AWS_STORAGE_URL = 'media.safebee.com'
AWS_STATIC_BUCKET_NAME = 'static.dev.safebee.com'
AWS_STATIC_URL = 'static.safebee.com'
AWS_HEADERS = {
    'Expires': 'Fri, 31 Dec 2031 23:59:59 GMT',
    'Cache-Control': 'max-age=2592000',
}
AWS_IS_GZIPPED = True

# S3-only keys
AWS_ACCESS_KEY_ID = "AKIAIS6QKO33FI26PXWA"
AWS_SECRET_ACCESS_KEY = "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"

AWS_S3_SECURE_URLS = False
AWS_S3_CUSTOM_DOMAIN = AWS_STORAGE_URL
AWS_STATIC_CUSTOM_DOMAIN = AWS_STATIC_URL
STATIC_URL = 'http://%s/' % AWS_STATIC_URL
COMPRESS_URL = STATIC_URL
MEDIA_URL = 'http://%s/' % AWS_STORAGE_URL

# Social Settings
TWITTER_API_KEY = 's6ExKElWtQIryJHiSe2Pkn2l9'
TWITTER_API_SECRET_KEY = 'nScTvTT9noWL2dQ5QaMiqsCWRwoKqvoT76zmqxlz8qPFCUHRLj'
TWITTER_OAUTH_ACCESS_TOKEN = '2915852673-6Il59i6zIgfy6XJp8Ov9FOeSvmKtjs5o2B5ikiw'
TWITTER_OAUTH_SECRET_TOKEN = 'tWhx6BlcjjmpEU6QsZKzO0tbgw8njgXovM5pdcnYcs8FR'
BITLY_CUSTOM_DOMAIN = ''

# Celery
BROKER_URL = 'django://'
CELERY_ALWAYS_EAGER = True

# Disqus
DISQUS_API_KEY = 'dvy5i3y9WLVk6tspOODnATH1msUUJ5To94H2JmKiWWvMMUfMOlau58S2Zo9sOpZ9'
DISQUS_API_SECRET = 'suWyloJERGxzIwAzHutfey5j80ph0G5oUKqEyBFeBmE1vX9RsY0bz3qw78WKAg5L'
DISQUS_FORUM_SHORTNAME = 'safebee'

# SharedCount API
SHAREDCOUNT_ENABLED = True
SHAREDCOUNT_API_ENDPOINT = 'http://plus.sharedcount.com/'
SHAREDCOUNT_API_KEY = '96719dac0e64f9b1598d36fc24e76404e66bf249'
SHAREDCOUNT_DISPLAY_LOWER_LIMIT = 0

# Sentry

RAVEN_CONFIG = {
    'dsn': 'http://8c8a6695597d4163abac43d1b89387d2:d35bc298bba743258cd68c3b94b83669@sentry.mnndev.com:80/4',
}
