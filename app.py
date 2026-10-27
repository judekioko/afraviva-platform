"""Entry point for the afraviva.com Passenger (cPanel Python App) process.

There's no shell access on this hosting plan, so `manage.py migrate` and
`manage.py collectstatic` can't be run by hand. Both are idempotent, so we
run them here at process start instead. Only this app (not the media/farms
subdomain shims) does this, so the two don't race each other against the
same database.

The host starts several worker processes at once, and running migrate +
collectstatic in every one of them made each restart slow and kept hitting
the plan's process limit. So the deploy writes the commit it shipped to
tmp/deploy-id, and those tasks run once per deploy: the first worker takes a
file lock and does the work, the rest wait for it and then skip. Delete
tmp/startup-done to force them to run again on the next restart.
"""

import logging
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django  # noqa: E402

django.setup()

from django.core.management import call_command  # noqa: E402

logger = logging.getLogger("passenger_wsgi")

TMP = Path(__file__).resolve().parent / "tmp"


def _run(command, **options):
    try:
        call_command(command, verbosity=0, **options)
        return True
    except Exception:
        logger.exception("%s failed at startup", command)
        return False


def _once_per_deploy():
    deploy_id_file, done_file = TMP / "deploy-id", TMP / "startup-done"
    deploy_id = deploy_id_file.read_text().strip() if deploy_id_file.exists() else "no-deploy-id"
    TMP.mkdir(exist_ok=True)
    try:
        import fcntl
    except ImportError:  # Windows dev machine: no other workers to wait for.
        fcntl = None
    with open(TMP / "startup.lock", "w") as lock:
        if fcntl:
            fcntl.flock(lock, fcntl.LOCK_EX)
        if done_file.exists() and done_file.read_text().strip() == deploy_id:
            return
        ok = _run("migrate", interactive=False)
        ok = _run("collectstatic", interactive=False) and ok
        _run("twofa_status")
        if ok:  # A failure is retried on the next restart.
            done_file.write_text(deploy_id)


def _purge_daily():
    """Delete personal data past its retention period, at most once a day
    (see enquiries/management/commands/purge_expired_data.py)."""
    stamp = TMP / "last-purge"
    if stamp.exists() and time.time() - stamp.stat().st_mtime < 86400:
        return
    stamp.touch()  # first, so other workers starting now skip it
    _run("purge_expired_data")


_once_per_deploy()
_purge_daily()
# Cheap, and must notice a tmp/admin-recovery request on any restart.
_run("bootstrap_admin")

from django.core.wsgi import get_wsgi_application  # noqa: E402

_django_app = get_wsgi_application()


def application(environ, start_response):
    # Scanners send URLs that aren't valid UTF-8; Django's WSGI handler raises
    # UnicodeDecodeError decoding them before any middleware runs, which the
    # server turns into a 500. Answer 400 Bad Request instead.
    try:
        return _django_app(environ, start_response)
    except UnicodeDecodeError:
        start_response("400 Bad Request", [("Content-Type", "text/plain; charset=utf-8")])
        return [b"Bad request"]
