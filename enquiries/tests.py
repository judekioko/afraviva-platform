from django.core import mail
from django.test import TestCase
from django.urls import reverse

from .models import Enquiry


class EnquirySubmissionTests(TestCase):
    def test_valid_submission_creates_enquiry_and_sends_email(self):
        response = self.client.post(reverse("enquiries:submit"), {
            "name": "Jane Doe",
            "email": "jane@example.com",
            "phone": "",
            "source_page": "contact",
            "message": "Hello, I have a question.",
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Enquiry.objects.count(), 1)
        self.assertEqual(len(mail.outbox), 1)

    def test_invalid_submission_does_not_create_enquiry(self):
        response = self.client.post(reverse("enquiries:submit"), {
            "name": "",
            "email": "not-an-email",
            "message": "",
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Enquiry.objects.count(), 0)
