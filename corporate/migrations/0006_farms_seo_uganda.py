# The Farms list page's search description was seeded in 0005 as "across
# Kenya and Uganda"; AfraViva Farms is in Uganda. Only the untouched seeded
# text is replaced, so a description someone already edited in the admin is
# left alone.

from django.db import migrations

OLD = (
    "AfraViva Farms pilots farm-to-market platforms and hands-on training for family and community "
    "farms across Kenya and Uganda."
)
NEW = (
    "AfraViva Farms pilots farm-to-market platforms and hands-on training for family and community "
    "farms in Uganda."
)


def forwards(apps, schema_editor):
    apps.get_model("corporate", "PageSEO").objects.filter(page="farms_list", meta_description=OLD).update(
        meta_description=NEW,
    )


def backwards(apps, schema_editor):
    apps.get_model("corporate", "PageSEO").objects.filter(page="farms_list", meta_description=NEW).update(
        meta_description=OLD,
    )


class Migration(migrations.Migration):

    dependencies = [
        ("corporate", "0005_seed_cms_content"),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
