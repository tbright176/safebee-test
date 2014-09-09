#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "loop.settings.local")
    sys.path.append(os.path.dirname(__file__))
    sys.path.append('/var/www/loop/src/loop/loop')
    sys.path.append('/var/www/loop/src/loop/loop/apps')

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
