# Attaches real photos, sourced from afraviva.com/africanext.biz's own
# asset library, to the seeded Media posts. blog1/blog2 match their exact
# topics (the podcast and live-stream posts); the remaining posts use
# AfraViva Media's two general branded images.

import os

from django.db import migrations
from django.core.files import File

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "seed_assets")

PHOTO_MAP = {
    "the-unsung-heroes-of-bungango": "media-general-1.jpeg",
    "a-life-of-service-celebrating-the-golden-jubilee-of-archbishop-emeritus-john-baptist-odama": "media-general-2.jpeg",
    "the-untold-story-of-the-uganda-martyrs": "media-general-1.jpeg",
    "the-untold-stories-of-the-pimolo-martyrs": "media-general-2.jpeg",
    "spreading-hope-through-a-faith-based-podcast-series": "faith-podcast-blog.jpeg",
    "live-streaming-worship-connects-global-communities": "community-stream-blog.jpeg",
}


def attach_photos(apps, schema_editor):
    MediaPost = apps.get_model("media_hub", "MediaPost")
    for slug, filename in PHOTO_MAP.items():
        try:
            post = MediaPost.objects.get(slug=slug)
        except MediaPost.DoesNotExist:
            continue
        path = os.path.join(ASSETS_DIR, filename)
        with open(path, "rb") as f:
            post.cover_image.save(filename, File(f), save=True)


def detach_photos(apps, schema_editor):
    MediaPost = apps.get_model("media_hub", "MediaPost")
    MediaPost.objects.filter(slug__in=PHOTO_MAP.keys()).update(cover_image="")


class Migration(migrations.Migration):

    dependencies = [
        ('media_hub', '0003_real_media_stories'),
    ]

    operations = [
        migrations.RunPython(attach_photos, detach_photos),
    ]
