# Unpublishes the five launch-placeholder farm updates seeded in 0002. They
# describe Kenya/Nairobi farms, but AfraViva Farms is in Uganda. The rows stay
# in the admin, so any of them can be edited and republished later.

from django.db import migrations

SLUGS = [
    "launching-farm-to-market-platforms-across-kenya-and-uganda",
    "strengthening-food-security-through-smallholder-partnerships",
    "training-program-equips-farmers-with-digital-tools",
    "a-season-of-growth-reviewing-our-first-agribusiness-pilot",
    "sustainable-practices-for-a-resilient-harvest",
]


def unpublish(apps, schema_editor):
    apps.get_model("farms_hub", "FarmUpdate").objects.filter(slug__in=SLUGS).update(is_published=False)


def republish(apps, schema_editor):
    apps.get_model("farms_hub", "FarmUpdate").objects.filter(slug__in=SLUGS).update(is_published=True)


class Migration(migrations.Migration):

    dependencies = [
        ("farms_hub", "0010_set_september_2026_location"),
    ]

    operations = [
        migrations.RunPython(unpublish, republish),
    ]
