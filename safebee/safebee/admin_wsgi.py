"""
WSGI config for loop project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/dev/howto/deployment/wsgi/
"""

import os, sys

sys.path.append(os.path.dirname(__file__))
sys.path.append('/srv/www/Loop/loop/')
sys.path.append('/srv/www/Loop/loop/loop')
sys.path.append('/srv/www/Loop/loop/loop/apps')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "loop.settings.admin")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
