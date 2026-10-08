# Keyword-focused page titles and search descriptions (chosen 2026-10-08),
# so each page tells search engines what it's about. Stored in PageSEO, so
# staff can keep adjusting them under Admin > Page SEO.

from django.db import migrations

SEO = {
    "home": (
        "AfraViva — Media, Homes & Farms Across Africa | AfricaNext Opportunities",
        "AfraViva, the brand of AfricaNext Opportunities (ANO), builds purpose-driven businesses across Africa: youth media, homes in Nairobi and farms in Uganda.",
    ),
    "media_list": (
        "AfraViva Media — Catholic Pro-Life & Pro-Family Youth Media in Kenya",
        "AfraViva Media is a Catholic pro-life, pro-family youth media house in Nairobi, Kenya, creating content on faith, family and religious freedom for Africa.",
    ),
    "farms_list": (
        "AfraViva Farms — Farm-to-Market & Farmer Training in Uganda",
        "AfraViva Farms runs farm-to-market platforms and hands-on farmer training with family and community farms in Uganda. Real updates from the field.",
    ),
    "services": (
        "Media, Real Estate & Business Development Services in Nairobi | AfraViva",
        "AfraViva services in Nairobi: youth media production, model residences and real estate, farm-to-market agribusiness and business development across Africa.",
    ),
    "about": (
        "About AfraViva & AfricaNext Opportunities (ANO) — Nairobi, Kenya",
        "AfraViva is the brand of AfricaNext Opportunities (ANO), a Nairobi company building sustainable businesses in media, homes, farms and community development.",
    ),
    "thrivepoint": (
        "ThrivePoint Insights — African Business Growth Reports & Trends",
        "ThrivePoint Insights by AfraViva: reports, guides and trends on African business growth, investment and opportunity across the continent.",
    ),
    "contact": (
        "Contact AfraViva — St. Joseph Studio, Ngong Road, Nairobi",
        "Contact AfraViva at St. Joseph Studio, Covenant Road, off Ngong Road, Nairobi, Kenya, for media, homes, farms and business development enquiries.",
    ),
}


def apply(apps, schema_editor):
    PageSEO = apps.get_model("corporate", "PageSEO")
    for page, (title, description) in SEO.items():
        PageSEO.objects.update_or_create(page=page, defaults={"title": title, "meta_description": description})


class Migration(migrations.Migration):

    dependencies = [
        ("corporate", "0008_links_to_afravivamedia"),
    ]

    operations = [
        migrations.RunPython(apply, migrations.RunPython.noop),
    ]
