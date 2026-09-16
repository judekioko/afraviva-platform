from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import MediaPost


class MediaPostTests(TestCase):
    def test_slug_is_generated_from_title(self):
        post = MediaPost.objects.create(title="Hello World", body="Body text")
        self.assertEqual(post.slug, "hello-world")

    def test_unpublished_post_returns_404(self):
        post = MediaPost.objects.create(title="Draft post", body="Body", is_published=False)
        response = self.client.get(post.get_absolute_url())
        self.assertEqual(response.status_code, 404)

    def test_published_post_is_visible(self):
        post = MediaPost.objects.create(
            title="Published post", body="Body", is_published=True, published_at=timezone.now()
        )
        response = self.client.get(post.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Published post")

    def test_list_view_loads(self):
        response = self.client.get(reverse("media_hub:list"))
        self.assertEqual(response.status_code, 200)
