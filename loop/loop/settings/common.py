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
PROJECT_ENV = 'Test'
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
    'django.contrib.humanize',
    'django.contrib.redirects',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',

    'compressor',
    'easy_thumbnails',
    'easy_thumbnails.optimize',
    'micawber.contrib.mcdjango',
    'reversion',
    'watson',
    'locking',

    'social',
    'asset_manager',
    'buzz',
    'core',
    'features',
    'flatpages',
    'hubpage',
    'mastermind',
    'rail_manager',
    'recalls',
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
    'core.context_processors.debug_status',
)

TEMPLATE_DIRS = (
    os.path.join(PROJECT_DIR, 'templates'),
)

ROOT_URLCONF = 'loop.urls'

WSGI_APPLICATION = 'loop.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

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
CORE_DEFAULT_FEED_LENGTH = 70
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
        'default_content_well': {'size': (838, 0)},
    },
}
THUMBNAIL_QUALITY = 67
THUMBNAIL_OPTIMIZE_COMMAND = {
    'jpeg': '/usr/bin/jpegoptim {filename}',
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
BITLY_API_USER = 'bensafebee'
BITLY_API_KEY = 'R_f4b7ac28682d4b6ea5a8dc3c952fd9cb'

# Chartbeat
CHARTBEAT_API_URL = 'http://api.chartbeat.com/live/toppages/v3/'
CHARTBEAT_API_KEY = ''
CHARTBEAT_API_HOST = ''

# LOOP-120, staging site link removal from content
STAGING_SITE_HOSTNAME = 'staging.safebee.com'

# SharedCount API
SHAREDCOUNT_ENABLED = True
SHAREDCOUNT_API_ENDPOINT = 'http://free.sharedcount.com/'
SHAREDCOUNT_API_KEY = '96719dac0e64f9b1598d36fc24e76404e66bf249'
SHAREDCOUNT_DISPLAY_LOWER_LIMIT = 0

# MailChimp
MAILCHIMP_URL = 'http://mnn.us4.list-manage.com/subscribe/post?u=6df70d8dcc50e45d16f196d8c&amp;id=6e238acf12'
RECALL_SIGNUP_MAILCHIMP_URL = 'http://mnn.us4.list-manage.com/subscribe/post?u=6df70d8dcc50e45d16f196d8c&amp;id=837709b1b0'

# Misc
BLOG_DISCLAIMER = """The opinions expressed in blogs and reader comments are those of the writers and do not reflect the opinions of <a href="http://www.safebee.com">SafeBee.com</a>. While we have reviewed the content to ensure it complies with our <a href="http://www.safebee.com/terms/">Terms and Conditions</a>, SafeBee is not responsible for the accuracy of any of the information."""

# Recall Settings
SNS_TOPIC_PREFIX = 'SB-{}'.format(PROJECT_ENV)
SNS_TOPIC_RECALL_NEWSLETTER = 'Safebee-Recalls'

# UL Feed Settings
UL_NEWS_FEED = 'http://ul.com/newsroom/publicnotices/feed/'

# django-locking
LOCKING = {'time_until_expiration': 120, 'time_until_warning': 60}

# RSS Settings
POPULAR_FEED_CATEGORY_ORDER = ["Home", "Health", "Food", "Family", "Outdoors", "Money", "Tech", "Travel"]