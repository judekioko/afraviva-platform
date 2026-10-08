# afravivamedia.com is now the main Media address (media.afraviva.com 301s
# to it). Point every saved link that used the old host at the new one, so
# visitors and search engines skip the redirect.

from django.db import migrations

OLD = "https://media.afraviva.com"
NEW = "https://afravivamedia.com"

FIELDS = [
    ("SiteSettings", "media_url"),
    ("NavLink", "external_url"),
    ("SocialLink", "url"),
    ("ServiceCard", "link_url"),
    ("InsightPublication", "external_url"),
]


def swap(apps, old, new):
    for model_name, field in FIELDS:
        model = apps.get_model("corporate", model_name)
        for obj in model.objects.filter(**{f"{field}__startswith": old}):
            setattr(obj, field, new + getattr(obj, field)[len(old):])
            obj.save(update_fields=[field])


def forwards(apps, schema_editor):
    swap(apps, OLD, NEW)


def backwards(apps, schema_editor):
    swap(apps, NEW, OLD)


class Migration(migrations.Migration):

    dependencies = [
        ("corporate", "0007_media_url_default_afravivamedia"),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
