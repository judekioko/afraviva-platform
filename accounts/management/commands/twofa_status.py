"""Logs which active staff accounts have a confirmed TOTP device.

ADMIN_REQUIRE_2FA must only be switched on once every active staff account
has one, or anyone without a device is locked out of the admin. There's no
shell or working phpMyAdmin on this host, so app.py runs this at startup and
the answer lands in the server's stderr.log.
"""

import logging

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django_otp.plugins.otp_totp.models import TOTPDevice

logger = logging.getLogger("passenger_wsgi")


def staff_without_2fa():
    staff = get_user_model().objects.filter(is_active=True, is_staff=True)
    enrolled = set(TOTPDevice.objects.filter(confirmed=True).values_list("user_id", flat=True))
    return staff, [u for u in staff if u.pk not in enrolled]


class Command(BaseCommand):
    help = "Reports whether every active staff account has two-step login set up."

    def handle(self, *args, **options):
        staff, missing = staff_without_2fa()
        if missing:
            message = (
                f"2FA readiness: {staff.count() - len(missing)} of {staff.count()} active staff have "
                f"two-step login; not yet: {', '.join(u.username for u in missing)}"
            )
        else:
            message = f"2FA readiness: all {staff.count()} active staff have two-step login — safe to enable"
        logger.warning(message)
        self.stdout.write(message)
