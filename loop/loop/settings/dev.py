from .common import *


DEBUG = True
TEMPLATE_DEBUG = DEBUG
COMPRESS_ENABLED = False
THUMBNAIL_DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'safebee',
    },
}

INSTALLED_APPS += (
    'debug_toolbar.apps.DebugToolbarConfig',
    'django_extensions',
    'devserver',
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

# Social Settings
TWITTER_API_KEY = ''
TWITTER_API_SECRET_KEY = ''
TWITTER_OAUTH_ACCESS_TOKEN = ''
TWITTER_OAUTH_SECRET_TOKEN = ''
BITLY_CUSTOM_DOMAIN = ''
