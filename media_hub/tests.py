from urllib.parse import urlparse

from django.conf import settings
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from .models import FeaturedTikTok, MediaPost


# media.afraviva.com / afravivamedia.com mount this app at the domain root
# (see config/urls_media.py) — every other domain (including the test
# client's default "testserver") uses the main urlconf, which doesn't
# include media_hub at all, so these tests simulate the subdomain's own
# urlconf *and* Host header together — the corporate-link fallback in
# base.html keys off the real request host, not just the active urlconf.
@override_settings(ROOT_URLCONF="config.urls_media", ALLOWED_HOSTS=["afravivamedia.com", "media.afraviva.com"])
class MediaPostTests(TestCase):
    def test_slug_is_generated_from_title(self):
        post = MediaPost.objects.create(title="Hello World", body="Body text")
        self.assertEqual(post.slug, "hello-world")

    def test_get_absolute_url_is_the_main_media_domain(self):
        post = MediaPost.objects.create(title="Hello World", body="Body text")
        self.assertEqual(post.get_absolute_url(), "https://afravivamedia.com/hello-world/")

    def test_unpublished_post_returns_404(self):
        post = MediaPost.objects.create(title="Draft post", body="Body", is_published=False)
        response = self.client.get(urlparse(post.get_absolute_url()).path, HTTP_HOST="afravivamedia.com")
        self.assertEqual(response.status_code, 404)

    def test_published_post_is_visible(self):
        post = MediaPost.objects.create(
            title="Published post", body="Body", is_published=True, published_at=timezone.now()
        )
        response = self.client.get(urlparse(post.get_absolute_url()).path, HTTP_HOST="afravivamedia.com")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Published post")

    def test_list_view_loads(self):
        response = self.client.get(reverse("media_hub:list"), HTTP_HOST="afravivamedia.com")
        self.assertEqual(response.status_code, 200)

    @override_settings(MIDDLEWARE=["media_hub.middleware.redirect_to_main_media_domain"] + settings.MIDDLEWARE)
    def test_old_media_subdomain_redirects_permanently(self):
        response = self.client.get("/why-family/?page=2", HTTP_HOST="media.afraviva.com")
        self.assertEqual(response.status_code, 301)
        self.assertEqual(response["Location"], "https://afravivamedia.com/why-family/?page=2")

    def test_media_page_plays_featured_tiktoks_without_tiktok_scripts(self):
        FeaturedTikTok.objects.create(url="https://www.tiktok.com/@afravivamedia/video/7412345678901234567")
        response = self.client.get(reverse("media_hub:list"), HTTP_HOST="afravivamedia.com")
        self.assertContains(response, 'src="https://www.tiktok.com/player/v1/7412345678901234567?')
        self.assertNotContains(response, "embed.js")
        csp = response["Content-Security-Policy"]
        self.assertIn("frame-src 'self' https://www.youtube-nocookie.com https://player.vimeo.com https://www.tiktok.com", csp)
        self.assertIn("script-src 'self';", csp + ";")

    def test_media_page_without_featured_tiktoks_shows_only_the_banner(self):
        response = self.client.get(reverse("media_hub:list"), HTTP_HOST="afravivamedia.com")
        self.assertContains(response, "Follow @afravivamedia")
        self.assertNotContains(response, "tiktok.com/player")

    def test_featured_tiktok_needs_a_single_video_link(self):
        from django.core.exceptions import ValidationError

        with self.assertRaises(ValidationError):
            FeaturedTikTok(url="https://www.tiktok.com/@afravivamedia").full_clean()

    def test_posts_show_follow_banner_without_third_party_scripts(self):
        post = MediaPost.objects.create(title="Banner post", body="Body", is_published=True, published_at=timezone.now())
        response = self.client.get(f"/{post.slug}/", HTTP_HOST="afravivamedia.com")
        self.assertContains(response, "Follow @afravivamedia")
        self.assertNotContains(response, "tiktok.com/embed.js")
        self.assertNotIn("tiktok", response["Content-Security-Policy"])
