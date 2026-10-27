"""Deletes personal data past the retention periods in the Privacy Policy
(afraviva.com/privacy/, section 2):

- enquiries: 24 months after they were received
- staff access requests: 12 months after they were reviewed
- admin login records (django-axes): 90 days
- expired login sessions

app.py runs this about once a day, so the policy's "deleted automatically"
holds without shell access or a cron job (cron can't load the app's
environment variables on this host).
"""

import logging
from datetime import timedelta

from axes.models import AccessAttempt, AccessFailureLog, AccessLog
from django.contrib.sessions.models import Session
from django.core.management.base import BaseCommand
from django.utils import timezone

from accounts.models import SignupRequest
from enquiries.models import Enquiry

logger = logging.getLogger("passenger_wsgi")

ENQUIRY_DAYS = 730
SIGNUP_REQUEST_DAYS = 365
LOGIN_RECORD_DAYS = 90


class Command(BaseCommand):
    help = "Deletes personal data that is past its retention period."

    def handle(self, *args, **options):
        now = timezone.now()
        counts = {
            "enquiries": Enquiry.objects.filter(created_at__lt=now - timedelta(days=ENQUIRY_DAYS)).delete()[0],
            "staff access requests": SignupRequest.objects.filter(
                reviewed_at__lt=now - timedelta(days=SIGNUP_REQUEST_DAYS)
            ).delete()[0],
            "admin login records": sum(
                model.objects.filter(attempt_time__lt=now - timedelta(days=LOGIN_RECORD_DAYS)).delete()[0]
                for model in (AccessAttempt, AccessLog, AccessFailureLog)
            ),
            "expired sessions": Session.objects.filter(expire_date__lt=now).delete()[0],
        }
        summary = ", ".join(f"{n} {what}" for what, n in counts.items())
        logger.warning("Retention purge: deleted %s", summary)
        self.stdout.write(summary)
