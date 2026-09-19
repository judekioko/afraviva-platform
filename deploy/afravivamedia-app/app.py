"""Entry point for the media.afraviva.com / afravivamedia.com Passenger app.

This file lives in its own small "Application root" (a cPanel Python App
requirement — each app needs a distinct root), but it reuses the exact same
codebase, venv-installed packages and database as the main afraviva.com app.
It does NOT run migrate/collectstatic itself — the main app's
passenger_wsgi.py already does that against the same database.
"""

import os
import sys

MAIN_APP_DIR = "/home/dlapepda/afraviva-platform"
sys.path.insert(0, MAIN_APP_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings_media")

import django  # noqa: E402

django.setup()

from django.core.wsgi import get_wsgi_application  # noqa: E402

application = get_wsgi_application()
