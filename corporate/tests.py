import io

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from PIL import Image

from .validators import MAX_UPLOAD_SIZE_MB, validate_image_upload


def _make_image_file(name, size_px=(100, 100)):
    buf = io.BytesIO()
    Image.new("RGB", size_px).save(buf, format="PNG")
    return SimpleUploadedFile(name, buf.getvalue(), content_type="image/png")


class ImageUploadValidatorTests(TestCase):
    def test_normal_image_passes(self):
        validate_image_upload(_make_image_file("ok.png"))

    def test_oversized_file_is_rejected(self):
        f = _make_image_file("big.png")
        f.size = (MAX_UPLOAD_SIZE_MB + 1) * 1024 * 1024
        with self.assertRaises(ValidationError):
            validate_image_upload(f)

    def test_oversized_dimensions_are_rejected(self):
        f = _make_image_file("huge.png", size_px=(6001, 10))
        with self.assertRaises(ValidationError):
            validate_image_upload(f)


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


class SeoTests(TestCase):
    def test_main_site_sitemap_lists_corporate_pages(self):
        response = self.client.get("/sitemap.xml")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<loc>https://testserver/about/</loc>")

    def test_robots_points_at_this_domains_sitemap(self):
        response = self.client.get("/robots.txt")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sitemap: http://testserver/sitemap.xml")
        self.assertContains(response, "Disallow: /admin/")

    def test_pages_carry_share_preview_tags(self):
        response = self.client.get(reverse("corporate:about"))
        self.assertContains(response, '<meta property="og:title" content="About AfraViva &amp; AfricaNext Opportunities (ANO) — Nairobi, Kenya">')
        self.assertContains(response, 'og:image" content="http://testserver/static/img/share-default.jpg"')

    def test_pages_carry_organization_structured_data(self):
        import json
        import re

        html = self.client.get(reverse("corporate:about")).content.decode()
        (block,) = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
        data = json.loads(block)
        self.assertEqual((data["@type"], data["name"]), ("Organization", "AfraViva"))


class PrivacyPolicyTests(TestCase):
    def test_privacy_page_falls_back_to_contact_email_and_hides_blank_registration(self):
        from corporate.models import SiteSettings

        site = SiteSettings.load()
        response = self.client.get(reverse("corporate:privacy"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f"mailto:{site.contact_email}")
        self.assertNotContains(response, "ODPC registration number")
        self.assertNotContains(response, "Internal responsibilities")

    def test_privacy_settings_show_once_filled_in(self):
        from corporate.models import SiteSettings

        site = SiteSettings.load()
        site.privacy_email = "privacy@afraviva.com"
        site.odpc_registration_number = "ODPC/DC/123"
        site.save()
        response = self.client.get(reverse("corporate:privacy"))
        self.assertContains(response, "mailto:privacy@afraviva.com")
        self.assertContains(response, "ODPC/DC/123")

    def test_footer_and_contact_form_link_to_privacy_policy(self):
        response = self.client.get(reverse("corporate:contact"))
        self.assertContains(response, 'href="https://afraviva.com/privacy/"', count=2)


class MaintenanceModeTests(TestCase):
    def setUp(self):
        import tempfile
        from pathlib import Path
        from unittest import mock

        self.tmp = tempfile.TemporaryDirectory()
        self.flag = Path(self.tmp.name) / "maintenance"
        patcher = mock.patch("corporate.maintenance.FLAG", self.flag)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.addCleanup(self.tmp.cleanup)

    def test_sites_work_normally_without_the_flag(self):
        self.assertEqual(self.client.get("/").status_code, 200)

    def test_flag_shows_back_soon_page_with_503(self):
        self.flag.touch()
        response = self.client.get("/about/")
        self.assertEqual(response.status_code, 503)
        self.assertEqual(response["Retry-After"], "3600")
        self.assertContains(response, "We'll be back soon", status_code=503)

    def test_admin_login_stays_open(self):
        self.flag.touch()
        self.assertEqual(self.client.get("/admin/login/").status_code, 200)

    def test_media_and_farms_sites_also_go_offline(self):
        from django.test import override_settings

        self.flag.touch()
        for urlconf, host in [("config.urls_media", "afravivamedia.com"), ("config.urls_farms", "farms.afraviva.com")]:
            with override_settings(ROOT_URLCONF=urlconf, ALLOWED_HOSTS=[host]):
                self.assertEqual(self.client.get("/", HTTP_HOST=host).status_code, 503)
