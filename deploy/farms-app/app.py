"""Entry point for the farms.afraviva.com Passenger app.

This file lives in its own small "Application root" (a cPanel Python App
requirement — each app needs a distinct root), but it reuses the exact same
codebase, venv-installed packages and database as the main afraviva.com app.
It does NOT run migrate/collectstatic itself — the main app's
app.py already does that against the same database.
"""

import os
import sys

# Path to the main app on the server. Set MAIN_APP_DIR in the cPanel app's
# environment variables, or leave it unset to use ~/afraviva-platform
# (Passenger runs as the account user, so ~ is that account's home directory).
MAIN_APP_DIR = os.environ.get("MAIN_APP_DIR") or os.path.expanduser("~/afraviva-platform")
sys.path.insert(0, MAIN_APP_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings_farms")

import django  # noqa: E402

django.setup()

from django.core.wsgi import get_wsgi_application  # noqa: E402

application = get_wsgi_application()
