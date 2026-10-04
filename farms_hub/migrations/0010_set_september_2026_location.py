from django.db import migrations

SLUG = "tomato-harvest-and-new-maize-september-2026"


def set_location(apps, schema_editor):
    apps.get_model("farms_hub", "FarmUpdate").objects.filter(slug=SLUG).update(location="Uganda")


def clear_location(apps, schema_editor):
    apps.get_model("farms_hub", "FarmUpdate").objects.filter(slug=SLUG).update(location="")


class Migration(migrations.Migration):

    dependencies = [
        ("farms_hub", "0009_seed_september_2026_harvest"),
    ]

    operations = [
        migrations.RunPython(set_location, clear_location),
    ]
