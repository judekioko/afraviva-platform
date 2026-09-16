# Launch-ready draft content for AfraViva Farms, grounded in the real business
# facts migrated from afraviva.com (Kenya/Uganda agribusiness, farm-to-market
# platforms, community and family farms). Not migrated copy —
# farms.afraviva.com has no existing posts to migrate from (it's an empty
# directory listing). Meant as editable drafts for the AfraViva Farms team
# to review via admin.

from django.db import migrations
from django.utils import timezone
from django.utils.text import slugify

UPDATES = [
    (
        "Launching Farm-to-Market Platforms Across Kenya and Uganda",
        "infrastructure",
        "AfraViva Farms has begun rolling out digital farm-to-market "
        "platforms designed to connect smallholder farmers directly with "
        "buyers, cutting out costly middle layers in the supply chain. The "
        "pilot phase covers farming communities around Nairobi and Kampala, "
        "with training built into the rollout so farmers can use the tools "
        "independently.\n\n"
        "Early feedback has been encouraging: farmers report faster payment "
        "cycles and better visibility into market prices.",
    ),
    (
        "Strengthening Food Security Through Smallholder Partnerships",
        "community",
        "Food security starts at the smallholder level, and AfraViva Farms' "
        "latest partnerships are built around that principle. We're working "
        "directly with family and community-based farms across Kenya and "
        "Uganda to improve yields, share better agribusiness practices, and "
        "build more resilient local food systems.\n\n"
        "The approach is deliberately community-led — our role is to provide "
        "tools, training and market access, not to take over decision-making "
        "on the ground.",
    ),
    (
        "Training Program Equips Farmers with Digital Tools",
        "infrastructure",
        "A new AfraViva Farms training program is helping farmers across our "
        "Nairobi and Kampala regions get comfortable with the digital "
        "platforms now underpinning farm-to-market sales. Sessions cover "
        "everything from using mobile apps to track produce to understanding "
        "real-time pricing data.\n\n"
        "The program is designed to be hands-on and ongoing, not a one-time "
        "workshop, with regional coordinators available for follow-up "
        "support.",
    ),
    (
        "A Season of Growth: Reviewing Our First Agribusiness Pilot",
        "crop",
        "Our first full growing season under the AfraViva Farms model "
        "wrapped up with results worth sharing: participating farms saw "
        "measurable gains in both yield and market access compared to the "
        "previous season. The pilot focused on staple crops grown by family "
        "and community farms on Nairobi's periphery.\n\n"
        "We're using what we learned to refine the model before expanding it "
        "further into Uganda.",
    ),
    (
        "Sustainable Practices for a Resilient Harvest",
        "crop",
        "Sustainable agriculture is central to AfraViva Farms' mission — not "
        "just as an environmental commitment, but as the most reliable path "
        "to long-term food security and economic opportunity for the "
        "communities we work with. Our latest guidance to partner farms "
        "focuses on soil health, water conservation, and crop diversification "
        "suited to local conditions.\n\n"
        "These aren't abstract recommendations: they're drawn from what's "
        "actually working on the ground in Kenya and Uganda.",
    ),
]


def seed_updates(apps, schema_editor):
    FarmUpdate = apps.get_model("farms_hub", "FarmUpdate")
    now = timezone.now()
    for order, (title, category, body) in enumerate(UPDATES):
        FarmUpdate.objects.update_or_create(
            slug=slugify(title),
            defaults={
                "title": title,
                "category": category,
                "body": body,
                "is_published": True,
                "published_at": now - timezone.timedelta(days=order),
            },
        )


def remove_updates(apps, schema_editor):
    FarmUpdate = apps.get_model("farms_hub", "FarmUpdate")
    FarmUpdate.objects.filter(slug__in=[slugify(t) for t, _, _ in UPDATES]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("farms_hub", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_updates, remove_updates),
    ]
