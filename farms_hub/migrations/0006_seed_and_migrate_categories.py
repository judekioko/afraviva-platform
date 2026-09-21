# Seeds FarmCategory with the same four categories the old CATEGORY_CHOICES
# hardcoded, then points every existing FarmUpdate at the matching row.

from django.db import migrations

CATEGORIES = [
    ("crop", "Crop"),
    ("livestock", "Livestock"),
    ("infrastructure", "Infrastructure"),
    ("community", "Community"),
]


def seed_and_migrate(apps, schema_editor):
    FarmCategory = apps.get_model("farms_hub", "FarmCategory")
    FarmUpdate = apps.get_model("farms_hub", "FarmUpdate")

    slug_to_category = {}
    for order, (slug, name) in enumerate(CATEGORIES):
        category, _ = FarmCategory.objects.get_or_create(
            slug=slug, defaults={"name": name, "order": order},
        )
        slug_to_category[slug] = category

    for update in FarmUpdate.objects.all():
        category = slug_to_category.get(update.category)
        if category:
            update.category_fk = category
            update.save(update_fields=["category_fk"])


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("farms_hub", "0005_farmcategory"),
    ]

    operations = [
        migrations.RunPython(seed_and_migrate, noop_reverse),
    ]
