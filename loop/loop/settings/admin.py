CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
        'LOCATION': [
            '127.0.0.1:11211',
        ],
    },
}

ALLOWED_HOSTS = ['*']

# Cache override
CACHE_CONTROL_MAX_AGE = 0

# SharedCount API
SHAREDCOUNT_ENABLED = False
