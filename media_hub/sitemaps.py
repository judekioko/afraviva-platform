from django.contrib.sitemaps import Sitemap

from .models import MediaPost


class MediaSitemap(Sitemap):
    protocol = "https"

    def items(self):
        return [None] + list(MediaPost.objects.filter(is_published=True))

    def location(self, item):
        # A path, not get_absolute_url(), which returns a full URL.
        return "/" if item is None else f"/{item.slug}/"

    def lastmod(self, item):
        return None if item is None else item.updated_at
