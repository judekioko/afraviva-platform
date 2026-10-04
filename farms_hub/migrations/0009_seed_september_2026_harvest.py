# Publishes the September 2026 farm update with the real photos taken on the
# farm on 19 Sept 2026 (tomato harvest, tomato plots, and young maize).

import datetime
import os

from django.core.files import File
from django.db import migrations

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "seed_assets", "harvest-sept-2026")

SLUG = "tomato-harvest-and-new-maize-september-2026"
TITLE = "Tomato Harvest and New Maize: September on the Farm"
BODY = (
    "September brought our first real tomato harvest in from the field. "
    "Wheelbarrows and buckets of ripe fruit are now being sorted in the "
    "store, laid out on dry grass so they finish ripening evenly and don't "
    "bruise before they go to market.\n\n"
    "Out in the plots, the next tomato rows are flowering and setting fruit. "
    "We've mulched heavily with dry grass around each plant to hold moisture "
    "in the soil, keep weeds down, and stop fruit from sitting on bare "
    "ground.\n\n"
    "Alongside the tomatoes, a new maize crop is up and growing. The field "
    "team has been out weeding and earthing up the young plants while the "
    "rains hold.\n\n"
    "Here's how the farm looked on 19 September 2026."
)
COVER = "01-tomato-harvest-store.jpg"
PHOTOS = [
    ("01-tomato-harvest-store.jpg", "Freshly harvested tomatoes sorted in the store"),
    ("02-maize-field-crew.jpg", "The field team working the new maize crop"),
    ("03-maize-rows.jpg", "Young maize coming up in rows"),
    ("04-tomato-field.jpg", "Tomato plots mulched with dry grass"),
    ("05-tomato-flowering.jpg", "Tomato plants in flower"),
    ("06-tomato-fruit-set.jpg", "First fruit setting on a young plant"),
    ("07-tomato-young-fruit.jpg", "Green fruit forming along the stem"),
    ("08-tomato-mulched.jpg", "Mulch keeps the soil moist and weeds down"),
    ("09-tomatoes-ripening.jpg", "Tomatoes ripening on the vine"),
    ("10-tomatoes-turning.jpg", "Fruit turning from green to orange"),
    ("11-tomatoes-on-vine.jpg", "A cluster ready for picking"),
]


def seed(apps, schema_editor):
    FarmUpdate = apps.get_model("farms_hub", "FarmUpdate")
    FarmPhoto = apps.get_model("farms_hub", "FarmPhoto")
    FarmCategory = apps.get_model("farms_hub", "FarmCategory")

    update, _ = FarmUpdate.objects.update_or_create(
        slug=SLUG,
        defaults={
            "title": TITLE,
            "body": BODY,
            "category": FarmCategory.objects.filter(slug="crop").first(),
            "is_published": True,
            "published_at": datetime.datetime(2026, 9, 19, 14, 0, tzinfo=datetime.timezone.utc),
        },
    )
    with open(os.path.join(ASSETS_DIR, COVER), "rb") as f:
        update.cover_image.save(COVER, File(f), save=True)

    update.photos.all().delete()
    for order, (filename, caption) in enumerate(PHOTOS):
        photo = FarmPhoto(update=update, caption=caption, order=order)
        with open(os.path.join(ASSETS_DIR, filename), "rb") as f:
            photo.image.save(filename, File(f), save=True)


def unseed(apps, schema_editor):
    apps.get_model("farms_hub", "FarmUpdate").objects.filter(slug=SLUG).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("farms_hub", "0008_farmphoto"),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
