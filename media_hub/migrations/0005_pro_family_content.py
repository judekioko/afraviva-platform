# Adds two pro-family posts reflecting AfraViva Media's pro-life, pro-family
# editorial stance. No such photo exists yet on afraviva.com's own asset
# library, so these are sourced from Unsplash (free license, no attribution
# required) rather than fabricated or guessed.

import os

from django.db import migrations
from django.utils import timezone
from django.utils.text import slugify
from django.core.files import File

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "seed_assets")

POSTS = [
    (
        "Why Family Still Comes First",
        "family-picnic.jpg",
        "In a media landscape that often treats family as an afterthought, AfraViva "
        "Media puts it at the center. This piece looks at what it means to build "
        "content that strengthens family bonds rather than pulling them apart — "
        "starting with the everyday moments that rarely make headlines: a picnic, "
        "a shared afternoon, a family simply choosing to be together.\n\n"
        "It's a small story, but it's exactly the kind AfraViva Media exists to tell.",
    ),
    (
        "New Life, New Joy: Celebrating Young Families",
        "family-with-baby.jpg",
        "Every new child is a reason for celebration, and AfraViva Media's pro-life "
        "editorial stance means we make space for those stories — young parents "
        "navigating the joy and exhaustion of a new baby, grandparents meeting a "
        "grandchild for the first time, communities rallying around growing "
        "families.\n\n"
        "These are the stories that rarely trend, but they're the ones that matter "
        "most to the people living them.",
    ),
]


def add_family_posts(apps, schema_editor):
    MediaPost = apps.get_model("media_hub", "MediaPost")
    now = timezone.now()
    for order, (title, filename, body) in enumerate(POSTS):
        slug = slugify(title)
        post, _ = MediaPost.objects.update_or_create(
            slug=slug,
            defaults={
                "title": title,
                "body": body,
                "is_published": True,
                "published_at": now - timezone.timedelta(days=order),
            },
        )
        path = os.path.join(ASSETS_DIR, filename)
        with open(path, "rb") as f:
            post.cover_image.save(filename, File(f), save=True)


def remove_family_posts(apps, schema_editor):
    MediaPost = apps.get_model("media_hub", "MediaPost")
    MediaPost.objects.filter(slug__in=[slugify(t) for t, _, _ in POSTS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('media_hub', '0004_attach_real_photos'),
    ]

    operations = [
        migrations.RunPython(add_family_posts, remove_family_posts),
    ]
