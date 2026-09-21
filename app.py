"""Entry point for the afraviva.com Passenger (cPanel Python App) process.

There's no shell access on this hosting plan, so `manage.py migrate` and
`manage.py collectstatic` can't be run by hand. Both are idempotent, so we
run them here at process start instead — every time this app (re)starts.
Only this app (not the media/farms subdomain shims) does this, so the two
don't race each other against the same database.
"""

import logging
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django  # noqa: E402

django.setup()

from django.core.management import call_command  # noqa: E402

logger = logging.getLogger("passenger_wsgi")

try:
    call_command("migrate", interactive=False, verbosity=0)
except Exception:
    logger.exception("manage.py migrate failed at startup")

try:
    call_command("collectstatic", interactive=False, verbosity=0)
except Exception:
    logger.exception("manage.py collectstatic failed at startup")

try:
    call_command("bootstrap_admin", verbosity=0)
except Exception:
    logger.exception("bootstrap_admin failed at startup")

from django.core.wsgi import get_wsgi_application  # noqa: E402

application = get_wsgi_application()
