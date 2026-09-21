# Creates the "Staff" group approved signups are added to: full CRUD on all
# CMS content models, but no access to Users/Groups/SignupRequest (account
# management stays super-admin-only) and no access to Enquiries (public
# contact-form submissions, which can carry names/emails/phone numbers).

from django.db import migrations

CONTENT_MODELS = [
    ("corporate", "sitesettings"),
    ("corporate", "navlink"),
    ("corporate", "sociallink"),
    ("corporate", "heroslide"),
    ("corporate", "servicecard"),
    ("corporate", "partnercard"),
    ("corporate", "visionpillar"),
    ("corporate", "aboutcard"),
    ("corporate", "insightpublication"),
    ("corporate", "officelocation"),
    ("corporate", "pageseo"),
    ("corporate", "faqitem"),
    ("corporate", "teammember"),
    ("media_hub", "mediapost"),
    ("farms_hub", "farmupdate"),
    ("farms_hub", "farmcategory"),
]


def create_staff_group(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")
    ContentType = apps.get_model("contenttypes", "ContentType")

    group, _ = Group.objects.get_or_create(name="Staff")

    perms = []
    for app_label, model_name in CONTENT_MODELS:
        try:
            ct = ContentType.objects.get(app_label=app_label, model=model_name)
        except ContentType.DoesNotExist:
            continue
        perms.extend(Permission.objects.filter(content_type=ct))
    group.permissions.set(perms)


def remove_staff_group(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Group.objects.filter(name="Staff").delete()


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
        ("corporate", "0005_seed_cms_content"),
        ("media_hub", "0007_add_cms_models"),
        ("farms_hub", "0007_finalize_category_field"),
    ]

    operations = [
        migrations.RunPython(create_staff_group, remove_staff_group),
    ]
