# Replaces the generic launch-draft posts from 0002 with real story topics
# migrated from https://afraviva.com/Services/afravivamedia.php, which
# confirms AfraViva Media is a pro-life, pro-family, Catholic-leaning media
# house (references to Archbishop Emeritus John Baptist Odama, the Uganda
# Martyrs, and the Pimolo Martyrs are all real Catholic figures/history).

from django.db import migrations
from django.utils import timezone
from django.utils.text import slugify

OLD_TITLES = [
    "Why Faith-Based Media Matters for Africa's Youth",
    "Behind the Camera: How We Tell Stories That Matter",
    "Family, Faith and the Digital Generation",
    "AfraViva Media Expands Regional Coverage into Kampala",
    "Five Voices Shaping Conversations on Faith and Culture in East Africa",
]

POSTS = [
    (
        "The Unsung Heroes of Bungango",
        "In this heartfelt video testimonial, a resident of Bungango shares "
        "her transformative journey of rediscovering faith through the "
        "support of her local community. It's the kind of grounded, "
        "real-world story AfraViva Media exists to tell — faith renewed not "
        "in the abstract, but through the people around us.\n\n"
        "Watch the full testimonial on our video channel.",
    ),
    (
        "A Life of Service: Celebrating the Golden Jubilee of Archbishop Emeritus John Baptist Odama",
        "Archbishop Emeritus John Baptist Odama's fifty years of priestly and "
        "episcopal service were marked with a powerful sermon on resilience "
        "and hope, recorded during a live-streamed celebration that reached "
        "thousands across the region.\n\n"
        "AfraViva Media was honoured to help share this milestone in Ugandan "
        "Catholic life with a wider audience, in keeping with our mission to "
        "document faith stories that matter.",
    ),
    (
        "The Untold Story of the Uganda Martyrs",
        "A youth group came together to create a vibrant video retelling the "
        "story of the Uganda Martyrs, whose witness to faith remains a "
        "touchstone of Catholic life in the region more than a century "
        "later.\n\n"
        "Produced by young creators for a young audience, the piece is a "
        "reminder that the stories shaping East African faith and identity "
        "are still very much alive.",
    ),
    (
        "The Untold Stories of the Pimolo Martyrs",
        "This piece follows mission work connected to the Pimolo Martyrs, "
        "shared with a global audience through digital platforms that "
        "highlight faith-driven impact and community outreach.\n\n"
        "It's part of AfraViva Media's broader effort to bring lesser-known "
        "but significant stories of African Catholic history to a wider "
        "audience.",
    ),
    (
        "Spreading Hope Through a Faith-Based Podcast Series",
        "AfraViva Media partnered with a Christian media group to launch a "
        "podcast series sharing stories of resilience and faith, reaching "
        "thousands of listeners with messages of hope and inspiration.\n\n"
        "The series reflects our pro-life, pro-family editorial stance — "
        "content meant to strengthen, not undermine, the communities it "
        "reaches.",
    ),
    (
        "Live-Streaming Worship Connects Global Communities",
        "A local church embraced digital media to live-stream its services, "
        "uniting believers worldwide and fostering a vibrant online "
        "community of faith — the kind of connection AfraViva Media's "
        "production support makes possible.\n\n"
        "As more congregations look to extend their reach digitally, we're "
        "building the production know-how to help them do it well.",
    ),
]


def apply_real_stories(apps, schema_editor):
    MediaPost = apps.get_model("media_hub", "MediaPost")
    MediaPost.objects.filter(slug__in=[slugify(t) for t in OLD_TITLES]).delete()

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


def revert(apps, schema_editor):
    MediaPost = apps.get_model("media_hub", "MediaPost")
    MediaPost.objects.filter(slug__in=[slugify(t) for t, _ in POSTS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('media_hub', '0002_seed_launch_content'),
    ]

    operations = [
        migrations.RunPython(apply_real_stories, revert),
    ]
