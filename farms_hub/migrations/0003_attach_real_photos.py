# Attaches real farm/agribusiness photos, sourced from afraviva.com's own
# asset library, to the seeded Farm updates.

import os

from django.db import migrations
from django.core.files import File

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "seed_assets")

PHOTO_MAP = {
    "launching-farm-to-market-platforms-across-kenya-and-uganda": "agritwo.jpeg",
    "strengthening-food-security-through-smallholder-partnerships": "agrione.jpeg",
    "training-program-equips-farmers-with-digital-tools": "agribusiness.jpeg",
    "a-season-of-growth-reviewing-our-first-agribusiness-pilot": "agribusiness.jpeg",
    "sustainable-practices-for-a-resilient-harvest": "agrione.jpeg",
}


def attach_photos(apps, schema_editor):
    FarmUpdate = apps.get_model("farms_hub", "FarmUpdate")
    for slug, filename in PHOTO_MAP.items():
        try:
            update = FarmUpdate.objects.get(slug=slug)
        except FarmUpdate.DoesNotExist:
            continue
        path = os.path.join(ASSETS_DIR, filename)
        with open(path, "rb") as f:
            update.cover_image.save(filename, File(f), save=True)


def detach_photos(apps, schema_editor):
    FarmUpdate = apps.get_model("farms_hub", "FarmUpdate")
    FarmUpdate.objects.filter(slug__in=PHOTO_MAP.keys()).update(cover_image="")


class Migration(migrations.Migration):

    dependencies = [
        ('farms_hub', '0002_seed_launch_content'),
    ]

    operations = [
        migrations.RunPython(attach_photos, detach_photos),
    ]
