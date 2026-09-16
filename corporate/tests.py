from django.test import TestCase
from django.urls import reverse


class CorporatePagesTests(TestCase):
    def test_home_page_loads(self):
        response = self.client.get(reverse("corporate:home"))
        self.assertEqual(response.status_code, 200)

    def test_about_page_loads(self):
        response = self.client.get(reverse("corporate:about"))
        self.assertEqual(response.status_code, 200)

    def test_contact_page_loads(self):
        response = self.client.get(reverse("corporate:contact"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "enquiry-form-slot")

    def test_nav_never_points_homes_at_a_django_url(self):
        response = self.client.get(reverse("corporate:home"))
        self.assertContains(response, "https://homes.afraviva.com")
