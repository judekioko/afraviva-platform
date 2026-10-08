from django.test import TestCase, override_settings

from .models import FarmUpdate


@override_settings(ROOT_URLCONF="config.urls_farms", ALLOWED_HOSTS=["farms.afraviva.com"])
class FarmsSeoTests(TestCase):
    # The harvest post is published by migration 0009; the Kenya placeholders
    # are unpublished by 0011.
    harvest = "tomato-harvest-and-new-maize-september-2026"

    def setUp(self):
        # Pages only render subdomain-style links on a subdomain host.
        self.client.defaults["HTTP_HOST"] = "farms.afraviva.com"

    def test_sitemap_lists_only_published_updates(self):
        response = self.client.get("/sitemap.xml")
        self.assertContains(response, f"<loc>https://farms.afraviva.com/{self.harvest}/</loc>")
        self.assertNotContains(response, "across-kenya-and-uganda")

    def test_update_shares_its_cover_photo(self):
        update = FarmUpdate.objects.get(slug=self.harvest)
        response = self.client.get(f"/{self.harvest}/")
        self.assertContains(response, '<meta property="og:type" content="article">')
        self.assertContains(response, f'og:image" content="http://farms.afraviva.com{update.cover_image.url}"')

    def test_update_without_cover_falls_back_to_default_image(self):
        FarmUpdate.objects.filter(slug=self.harvest).update(cover_image="")
        response = self.client.get(f"/{self.harvest}/")
        self.assertContains(response, 'og:image" content="http://farms.afraviva.com/static/img/share-default.jpg"')

    def test_update_has_valid_article_structured_data(self):
        import json
        import re

        html = self.client.get(f"/{self.harvest}/").content.decode()
        blocks = [json.loads(b) for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)]
        self.assertEqual([b["@type"] for b in blocks], ["Article"])
        self.assertEqual(blocks[0]["headline"], "Tomato Harvest and New Maize: September on the Farm")
        self.assertEqual(blocks[0]["publisher"]["name"], "AfraViva")
        self.assertIn("datePublished", blocks[0])
