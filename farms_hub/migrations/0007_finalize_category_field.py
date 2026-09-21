# Drops the old hardcoded-choices CharField now that every row has been
# copied onto the new FarmCategory foreign key, then renames the FK into
# its permanent place.

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("farms_hub", "0006_seed_and_migrate_categories"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="farmupdate",
            name="category",
        ),
        migrations.RenameField(
            model_name="farmupdate",
            old_name="category_fk",
            new_name="category",
        ),
    ]
