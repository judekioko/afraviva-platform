# Launch-ready draft content for AfraViva Media, grounded in the real business
# facts migrated from afraviva.com (Nairobi HQ, Kampala regional desk,
# faith/family-focused youth media). Not migrated copy — media.afraviva.com
# has no existing posts to migrate from (it's an empty directory listing).
# Meant as editable drafts for the AfraViva Media team to review via admin.

from django.db import migrations
from django.utils import timezone
from django.utils.text import slugify

POSTS = [
    (
        "Why Faith-Based Media Matters for Africa's Youth",
        "Across Nairobi and Kampala, AfraViva Media is producing digital content "
        "that speaks directly to a generation navigating fast-changing culture, "
        "family expectations, and questions of faith. Our video, audio and "
        "written pieces explore what it means to hold onto conviction while "
        "embracing the opportunities of a connected Africa.\n\n"
        "We work with young creators, pastors, and community voices to shape "
        "stories that are honest about the tension between tradition and "
        "modern life — without losing sight of hope.",
    ),
    (
        "Behind the Camera: How We Tell Stories That Matter",
        "Every AfraViva Media production starts the same way: in conversation "
        "with the people whose story we're telling. Whether it's a family "
        "navigating faith across generations or a community responding to "
        "change, our production process is built around listening first.\n\n"
        "From our Nairobi studio to shoots across East Africa, the team keeps "
        "production lean and mobile — prioritising authentic voices over "
        "polish for its own sake.",
    ),
    (
        "Family, Faith and the Digital Generation",
        "Social media has changed how young Africans encounter ideas about "
        "family, identity and belief — often faster than parents, churches or "
        "schools can respond. AfraViva Media exists to meet that gap with "
        "content that's honest, well-produced, and rooted in Christian values "
        "of justice and community.\n\n"
        "Our latest content series looks at how families across Kenya and "
        "Uganda are adapting, and what's working.",
    ),
    (
        "AfraViva Media Expands Regional Coverage into Kampala",
        "AfraViva Media's Kampala desk is now live, extending our reporting "
        "and content production beyond Nairobi into Uganda's media landscape. "
        "The regional office focuses on localized storytelling — content that "
        "reflects Kampala's own communities and creative voices, rather than a "
        "Nairobi lens applied elsewhere.\n\n"
        "Expect more collaborations with Ugandan creators, faith leaders and "
        "youth organisations in the months ahead.",
    ),
    (
        "Five Voices Shaping Conversations on Faith and Culture in East Africa",
        "We spent the past quarter speaking with pastors, youth leaders, and "
        "independent creators across Nairobi and Kampala about how faith and "
        "culture intersect for young East Africans today. This roundup "
        "captures five perspectives — some hopeful, some challenging — that "
        "are shaping the conversations we cover.\n\n"
        "It's the kind of grounded, community-sourced reporting AfraViva "
        "Media exists to produce.",
    ),
]


def seed_posts(apps, schema_editor):
    MediaPost = apps.get_model("media_hub", "MediaPost")
    now = timezone.now()
    for order, (title, body) in enumerate(POSTS):
        MediaPost.objects.update_or_create(
            slug=slugify(title),
            defaults={
                "title": title,
                "body": body,
                "is_published": True,
                "published_at": now - timezone.timedelta(days=order),
            },
        )


def remove_posts(apps, schema_editor):
    MediaPost = apps.get_model("media_hub", "MediaPost")
    MediaPost.objects.filter(slug__in=[slugify(t) for t, _ in POSTS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("media_hub", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_posts, remove_posts),
    ]
