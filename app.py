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


_once_per_deploy()
# Cheap, and must notice a tmp/admin-recovery request on any restart.
_run("bootstrap_admin")

from django.core.wsgi import get_wsgi_application  # noqa: E402

application = get_wsgi_application()
