# Introduces FarmCategory as a real, admin-editable model, replacing the
# hardcoded CATEGORY_CHOICES on FarmUpdate. The new FK is added under a
# temporary name (category_fk) so the old 'category' CharField can keep
# existing data until 0006 copies it across.

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("farms_hub", "0004_alter_farmupdate_cover_image"),
    ]

    operations = [
        migrations.CreateModel(
            name="FarmCategory",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=60)),
                ("slug", models.SlugField(blank=True, max_length=60, unique=True)),
                ("order", models.PositiveIntegerField(default=0)),
                ("published", models.BooleanField(default=True)),
            ],
            options={
                "ordering": ["order", "id"],
                "verbose_name_plural": "Farm categories",
            },
        ),
        migrations.AddField(
            model_name="farmupdate",
            name="category_fk",
            field=models.ForeignKey(
                blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                related_name="updates", to="farms_hub.farmcategory",
            ),
        ),
    ]
