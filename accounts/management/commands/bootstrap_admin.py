"""Bootstrap / recovery for the AfraViva superuser account.

There's no shell access on this hosting plan, so `createsuperuser` can't be
run by hand, and (until at least one staff account exists) there's no way to
send an invite email either. This command creates the account the first time
it runs and logs a set-password link to the server's log file.

After that it only logs a link on request: create an empty file named
`admin-recovery` in the app's tmp/ folder (cPanel File Manager), restart the
afraviva.com app, and the link appears in stderr.log; the file is deleted so
it's a one-off. Logging a working takeover link on every restart meant anyone
who could read the log could take over the admin account.
"""

import logging
from pathlib import Path

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.management.base import BaseCommand
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

logger = logging.getLogger("passenger_wsgi")

SUPERUSER_EMAIL = "judekioko15@gmail.com"
RECOVERY_TRIGGER = Path(settings.BASE_DIR) / "tmp" / "admin-recovery"


class Command(BaseCommand):
    help = "Creates the initial AfraViva superuser account if it doesn't exist yet."

    def handle(self, *args, **options):
        User = get_user_model()
        user = User.objects.filter(email__iexact=SUPERUSER_EMAIL).first()

        if user is None:
            user = User(
                username=SUPERUSER_EMAIL, email=SUPERUSER_EMAIL,
                is_staff=True, is_superuser=True, is_active=True,
            )
            user.set_unusable_password()
            user.save()

        # Only for an account that has never set a password, or when someone
        # with File Manager access asked for one — see module docstring.
        # Doesn't touch user.password, so it never invalidates one already set.
        recovery_requested = RECOVERY_TRIGGER.exists()
        if user.has_usable_password() and not recovery_requested:
            return
        if recovery_requested:
            RECOVERY_TRIGGER.unlink()
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        link = f"https://afraviva.com/accounts/reset/{uid}/{token}/"
        logger.warning("AfraViva bootstrap: set-password link for %s: %s", SUPERUSER_EMAIL, link)
