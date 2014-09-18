"""
Django settings for loop project.


For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP

PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media')
MEDIA_URL = '/media/'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ja0t*ho&ea!e0@)i$3g-!f-iblvfpkt6p^8#3e$_h9l=jwar5%'

SITE_ID = 1

# Application definition

INSTALLED_APPS = (
    'suit',
    'suit_redactor',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.redirects',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',

    'compressor',
    'easy_thumbnails',
    'micawber.contrib.mcdjango',
    'reversion',

    'social',
    'asset_manager',
    'core',
    'flatpages',
    'hubpage',
    'mastermind',
    'rail_manager',
    'widgets',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'flatpages.middleware.FlatpageFallbackMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',
    'django.core.context_processors.static',
    'core.context_processors.site_processor',
)

TEMPLATE_DIRS = (
    os.path.join(PROJECT_DIR, 'templates'),
)

ROOT_URLCONF = 'loop.urls'

WSGI_APPLICATION = 'loop.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_ROOT = os.path.join(MEDIA_ROOT, 'static')
STATIC_URL = '/media/static/'
STATICFILES_DIRS = (os.path.join(PROJECT_DIR, 'static'),)
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
)

# Core Settings
AUTH_USER_MODEL = 'core.LoopUser'
CORE_DEFAULT_INDEX_LENGTH = 15  # number of content items on an index page
CORE_DEFAULT_SITE_TITLE_SEPARATOR = '|'

# Django Suit Settings
SUIT_CONFIG = {
    'ADMIN_NAME': 'SafeBee',
    'LIST_PER_PAGE': 100,
    'MENU_EXCLUDE': ('core.streamitem',),
}

# Easy Thumbnail settings
THUMBNAIL_ALIASES = {
    'asset_manager.Image': {
        'admin_change_list': {'size': (120, 80), 'crop': 'smart'},
        'facebook_social_image': {'size': (600, 315), 'crop': 'smart'},
        'default_content_well': {'size': (870, 0)},
    },
}

# django-compressor
COMPRESS_CSS_FILTERS = ['compressor.filters.cssmin.CSSMinFilter',
                        'compressor.filters.css_default.CssAbsoluteFilter']
COMPRESS_STORAGE = 'loop.storage.S3StaticStorage'

# Cache
CACHE_CONTROL_MAX_AGE = 60 * 5

# SharedCount API
SHAREDCOUNT_ENABLED = True
SHAREDCOUNT_API_ENDPOINT = 'http://free.sharedcount.com/'
SHAREDCOUNT_API_KEY = ''
SHAREDCOUNT_DISPLAY_LOWER_LIMIT = 5

# Bitly
BITLY_API_USER = ''
BITLY_API_KEY = ''

# Chartbeat
CHARTBEAT_API_URL = 'http://api.chartbeat.com/live/toppages/v3/'
CHARTBEAT_API_KEY = ''
CHARTBEAT_API_HOST = ''

# LOOP-120, staging site link removal from content
STAGING_SITE_HOSTNAME = 'staging.safebee.com'
