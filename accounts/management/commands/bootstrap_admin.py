"""Bootstrap / recovery for the AfraViva superuser account.

There's no shell access on this hosting plan, so `createsuperuser` can't be
run by hand, and (until at least one staff account exists) there's no way to
send an invite email either. This command creates the account the first time
it runs, and logs a fresh set-password link every time it runs — safe to
leave wired into every app startup (like migrate/collectstatic in app.py):
creating is idempotent, and re-logging a link for an existing account never
touches its current password, it just gives a way to log the account in via
the server's own log file without needing SMTP.
"""

import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.management.base import BaseCommand
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

logger = logging.getLogger("passenger_wsgi")

SUPERUSER_EMAIL = "judekioko15@gmail.com"


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

        # Re-logged every restart on purpose — see module docstring. Doesn't
        # touch user.password, so it never invalidates a password already set.
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        link = f"https://afraviva.com/accounts/reset/{uid}/{token}/"
        logger.warning("AfraViva bootstrap: set-password link for %s: %s", SUPERUSER_EMAIL, link)
