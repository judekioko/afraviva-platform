from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.test import TestCase
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .models import SignupRequest, StaffProfile


class SignupRequestFlowTests(TestCase):
    def test_signup_creates_pending_request(self):
        response = self.client.post(reverse("accounts:signup"), {
            "full_name": "Test Staffer", "email": "staffer@example.com", "hp_website": "",
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(SignupRequest.objects.filter(email="staffer@example.com", status="pending").exists())

    def test_honeypot_rejects_bots(self):
        response = self.client.post(reverse("accounts:signup"), {
            "full_name": "Bot", "email": "bot@example.com", "hp_website": "http://spam.example",
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(SignupRequest.objects.filter(email="bot@example.com").exists())

    def test_duplicate_email_rejected(self):
        get_user_model().objects.create_user(username="existing", email="existing@example.com")
        response = self.client.post(reverse("accounts:signup"), {
            "full_name": "Someone", "email": "existing@example.com", "hp_website": "",
        })
        self.assertContains(response, "already exists")


class ApproveActionTests(TestCase):
    def setUp(self):
        self.admin = get_user_model().objects.create_superuser("admin", "admin@example.com", "irrelevant-for-test")
        self.client.force_login(self.admin)
        self.signup = SignupRequest.objects.create(full_name="New Staffer", email="newstaffer@example.com")

    def test_approve_creates_staff_user_in_staff_group(self):
        changelist = reverse("admin:accounts_signuprequest_changelist")
        self.client.post(changelist, {
            "action": "approve_requests",
            "_selected_action": [str(self.signup.pk)],
        })
        self.signup.refresh_from_db()
        self.assertEqual(self.signup.status, SignupRequest.STATUS_APPROVED)

        user = get_user_model().objects.get(email="newstaffer@example.com")
        self.assertTrue(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.has_usable_password())
        self.assertTrue(user.groups.filter(name="Staff").exists())
        self.assertTrue(StaffProfile.objects.filter(user=user).exists())


class PasswordSetStampsProfileTests(TestCase):
    def test_setting_password_via_reset_link_stamps_profile(self):
        user = get_user_model().objects.create_user(username="staffer", email="staffer2@example.com")
        user.set_unusable_password()
        user.save()
        StaffProfile.objects.create(user=user)

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        # First GET redirects to the ?set-password form; follow it like a browser would.
        session_url = reverse("accounts:password_reset_confirm", kwargs={"uidb64": uid, "token": token})
        response = self.client.get(session_url, follow=True)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(response.request["PATH_INFO"], {
            "new_password1": "a-strong-generated-test-password-987",
            "new_password2": "a-strong-generated-test-password-987",
        })
        self.assertRedirects(response, reverse("accounts:password_reset_complete"))

        user.refresh_from_db()
        self.assertTrue(user.has_usable_password())
        profile = StaffProfile.objects.get(user=user)
        self.assertIsNotNone(profile.password_changed_at)


class PasswordExpiryMiddlewareTests(TestCase):
    def test_staff_with_no_profile_is_redirected_to_change_password(self):
        user = get_user_model().objects.create_user(
            username="expiredstaff", email="expired@example.com", password="whatever-not-checked-123", is_staff=True,
        )
        self.client.force_login(user)
        response = self.client.get(reverse("corporate:contact"))
        self.assertRedirects(response, reverse("accounts:password_change"), fetch_redirect_response=False)

    def test_superuser_is_exempt(self):
        admin = get_user_model().objects.create_superuser("admin2", "admin2@example.com", "whatever-not-checked-123")
        self.client.force_login(admin)
        response = self.client.get(reverse("corporate:contact"))
        self.assertEqual(response.status_code, 200)


class TwoFactorStatusTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.admin = User.objects.create_superuser("boss", "boss@example.com", "x")
        self.staffer = User.objects.create_user("staffer", "staffer@example.com", "x", is_staff=True)

    def test_status_names_staff_without_a_device(self):
        from accounts.management.commands.twofa_status import staff_without_2fa
        from django_otp.plugins.otp_totp.models import TOTPDevice

        TOTPDevice.objects.create(user=self.admin, name="phone", confirmed=True)
        _, missing = staff_without_2fa()
        self.assertEqual([u.username for u in missing], ["staffer"])

    def test_user_list_shows_two_step_column(self):
        self.client.force_login(self.admin)
        response = self.client.get("/admin/auth/user/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Two-step login")
