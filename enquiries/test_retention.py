import io
from datetime import timedelta

from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone

from accounts.models import SignupRequest
from enquiries.models import Enquiry


class RetentionPurgeTests(TestCase):
    def test_deletes_only_records_past_their_retention_period(self):
        old = Enquiry.objects.create(name="Old", email="old@example.com", message="hi")
        Enquiry.objects.filter(pk=old.pk).update(created_at=timezone.now() - timedelta(days=731))
        recent = Enquiry.objects.create(name="Recent", email="new@example.com", message="hi")
        reviewed = SignupRequest.objects.create(full_name="Reviewed", email="r@example.com", reviewed_at=timezone.now() - timedelta(days=366))
        pending = SignupRequest.objects.create(full_name="Pending", email="p@example.com")

        call_command("purge_expired_data", stdout=io.StringIO())

        self.assertFalse(Enquiry.objects.filter(pk=old.pk).exists())
        self.assertTrue(Enquiry.objects.filter(pk=recent.pk).exists())
        self.assertFalse(SignupRequest.objects.filter(pk=reviewed.pk).exists())
        self.assertTrue(SignupRequest.objects.filter(pk=pending.pk).exists())
