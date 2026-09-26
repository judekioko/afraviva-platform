# Seeds every new CMS model with the exact copy that used to be hardcoded in
# templates/context_processors/static JS, so the live site looks identical
# right after deploy. Staff then edit all of this from the admin from here on.

from django.db import migrations

NAV_LINKS = [
    ("Home", "home", "", 0),
    ("About", "about", "", 1),
    ("Services", "services", "", 2),
    ("Media", "", "https://media.afraviva.com", 3),
    ("Farms", "", "https://farms.afraviva.com", 4),
    ("ThrivePoint Insights", "thrivepoint", "", 5),
    ("FAQ", "faq", "", 6),
    ("Contact", "contact", "", 7),
    ("Homes", "", "https://homes.afraviva.com", 8),
]

SOCIAL_LINKS = [
    ("Facebook", "https://www.facebook.com/share/14iSWn76ZEr/", 0),
    ("Instagram", "https://www.instagram.com/afraviva_media", 1),
    ("TikTok", "https://www.tiktok.com/@afravivamedia", 2),
    ("YouTube", "https://www.youtube.com/@AfravivaMedia", 3),
    ("X", "https://x.com/AfravivaMedia", 4),
]

HERO_SLIDES = [
    (
        "Empowering Africa's Next Generation of Impact",
        "Blending talent, faith, and innovation to build sustainable businesses that uplift communities.",
        0,
    ),
    (
        "Uniting Africa's Visionaries for Progress",
        "Fostering growth and opportunity through purpose-driven investments and partnerships.",
        1,
    ),
    (
        "Transforming Africa's Future with Purpose",
        "Accelerating innovation and sustainability to create lasting change across the continent.",
        2,
    ),
]

SERVICE_CARDS = [
    (
        "AfraViva Media",
        "A pro-life, pro-family, Catholic-leaning media house producing youth-centric digital content on "
        "faith, family, and religious freedom, relevant to contemporary African society. Media partner: "
        "LifeSiteNews.",
        "Learn more →", "https://media.afraviva.com", 0,
    ),
    (
        "AfraViva Homes",
        "Invest in, design, and manage model residences well situated to key urban locations. Links to Airbnb.",
        "Visit homes.afraviva.com →", "https://homes.afraviva.com", 1,
    ),
    (
        "AfraViva Farms",
        "Our newest venture: piloting farm-to-market platforms and hands-on training for family and "
        "community farms across Kenya and Uganda.",
        "Learn more →", "https://farms.afraviva.com", 2,
    ),
    (
        "Business Development",
        "AfraViva is both a business accelerator for, and at times an investor in, new businesses focusing "
        "on the African market.",
        "Get in touch →", "/contact/", 3,
    ),
]

PARTNER_CARDS = [
    (
        "BYG Advantage",
        "Leading global sales accelerator focused on high-growth, tech-centric businesses seeking to "
        "expand into new markets.",
        0,
    ),
    (
        "OffChain — Global Web3 Community",
        "Bringing together professionals in Web3 and related AI, crypto, and blockchain industries "
        "through social and educational interactions.",
        1,
    ),
    (
        "Cash Kinetic (Kenya)",
        "Developer of a groundbreaking contactless payment device designed to digitize cash payments in Africa.",
        2,
    ),
]

VISION_PILLARS = [
    (
        "Agriculture",
        "To promote sustainable agriculture by enhancing food security and economic opportunities "
        "through innovative agribusiness practices.",
        0,
    ),
    (
        "Faith",
        "To inspire faith and hope by producing faith-based digital media content that promotes "
        "spiritual growth, healing, and transformation.",
        1,
    ),
    (
        "Hospitality",
        "To deliver exceptional hospitality by providing unique estate development consultancy "
        "services and curating unforgettable travel.",
        2,
    ),
    (
        "Community",
        "To foster community development by empowering local communities through job creation, "
        "skills development, and strategic partnerships.",
        3,
    ),
]

ABOUT_CARDS = [
    ("mission", "Agricultural Success", "Pioneering sustainable practices to cultivate resilience and prosperity in agriculture.", 0),
    ("mission", "Digital Content", "Crafting narratives that captivate, inform, and inspire vibrant communities.", 1),
    ("mission", "Estate Development", "Shaping sustainable estates with visionary guidance for enduring value.", 2),
    ("mission", "Business Development", "Empowering entrepreneurs with strategic expertise to scale and succeed.", 3),
    (
        "different", "Insurgent Mindset",
        "We work with ambitious clients who want to define the future, not hide from it. Together, we "
        "define a bold ambition and achieve extraordinary results that redefine industries.",
        0,
    ),
    (
        "different", "Integrated Innovation",
        "We deliver integrated solutions, complementing our capabilities with a curated ecosystem of the "
        "world's leading innovators to achieve better, faster, more enduring results for clients.",
        1,
    ),
    (
        "different", "Collaborative Culture",
        "It feels different to work with us because our people are unlike any other. We bring a fresh "
        "perspective, mutual trust, and infectious energy to every client relationship.",
        2,
    ),
]

INSIGHT_PUBLICATIONS = [
    ("Report", "African Business Growth Report 2025", "Strategies that redefine African markets.", "2025", 0),
    ("Guide", "SME Development Guide 2025", "Empowering the backbone of Africa's economy.", "2025", 1),
    ("Trends", "Market Expansion Trends 2025", "Where opportunity meets innovation.", "2025", 2),
]

OFFICE_LOCATIONS = [
    (
        "Nairobi HQ",
        "St. Joseph Studio, Covenant Road, off Ngong Road\nPast Dagoretti Corner, Nairobi, Kenya",
        "https://www.google.com/maps/search/?api=1&query=-1.3016022413838024,36.7544249110189",
        0,
    ),
]

PAGE_SEO = [
    (
        "home", "AfraViva — Where the World Meets Africa",
        "AfraViva, the brand of AfricaNext Opportunities (ANO) — blending talent, faith and innovation to "
        "build sustainable businesses across Media, Homes, Farms and Business Development.",
    ),
    (
        "about", "About — AfraViva",
        "AfraViva is the brand of AfricaNext Opportunities (ANO) — building sustainable, purpose-driven "
        "businesses across agribusiness, media, homes and community development in Africa.",
    ),
    (
        "services", "Services — AfraViva",
        "AfraViva's services: Media, Homes, Farms and Business Development — discover how we empower "
        "your goals with innovative expertise.",
    ),
    (
        "thrivepoint", "ThrivePoint Insights — AfraViva",
        "Sharp insights from AfraViva on Africa's future — reports, guides and trends on African "
        "business growth.",
    ),
    (
        "faq", "FAQ — AfraViva",
        "Answers to frequently asked questions about AfraViva's Media, Homes, Farms and Business "
        "Development services.",
    ),
    (
        "contact", "Contact — AfraViva",
        "Get in touch with AfraViva — our Nairobi, Kenya head office.",
    ),
    (
        "media_list", "Media — AfraViva",
        "AfraViva Media is a pro-life, pro-family, Catholic-leaning media house producing youth-centric "
        "digital content on faith, family and religious freedom.",
    ),
    (
        "farms_list", "Farms — AfraViva",
        "AfraViva Farms pilots farm-to-market platforms and hands-on training for family and community "
        "farms across Kenya and Uganda.",
    ),
]


def seed(apps, schema_editor):
    SiteSettings = apps.get_model("corporate", "SiteSettings")
    NavLink = apps.get_model("corporate", "NavLink")
    SocialLink = apps.get_model("corporate", "SocialLink")
    HeroSlide = apps.get_model("corporate", "HeroSlide")
    ServiceCard = apps.get_model("corporate", "ServiceCard")
    PartnerCard = apps.get_model("corporate", "PartnerCard")
    VisionPillar = apps.get_model("corporate", "VisionPillar")
    AboutCard = apps.get_model("corporate", "AboutCard")
    InsightPublication = apps.get_model("corporate", "InsightPublication")
    OfficeLocation = apps.get_model("corporate", "OfficeLocation")
    PageSEO = apps.get_model("corporate", "PageSEO")

    SiteSettings.objects.get_or_create(pk=1)

    for label, page, external_url, order in NAV_LINKS:
        NavLink.objects.update_or_create(
            label=label, defaults={"page": page, "external_url": external_url, "order": order, "published": True},
        )

    for label, url, order in SOCIAL_LINKS:
        SocialLink.objects.update_or_create(
            label=label, defaults={"url": url, "order": order, "published": True},
        )

    for headline, subhead, order in HERO_SLIDES:
        HeroSlide.objects.update_or_create(
            headline=headline, defaults={"subhead": subhead, "order": order, "published": True},
        )

    for title, description, link_label, link_url, order in SERVICE_CARDS:
        ServiceCard.objects.update_or_create(
            title=title,
            defaults={
                "description": description, "link_label": link_label, "link_url": link_url,
                "order": order, "published": True,
            },
        )

    for name, description, order in PARTNER_CARDS:
        PartnerCard.objects.update_or_create(
            name=name, defaults={"description": description, "order": order, "published": True},
        )

    for title, description, order in VISION_PILLARS:
        VisionPillar.objects.update_or_create(
            title=title, defaults={"description": description, "order": order, "published": True},
        )

    for section, title, description, order in ABOUT_CARDS:
        AboutCard.objects.update_or_create(
            section=section, title=title,
            defaults={"description": description, "order": order, "published": True},
        )

    for category_label, title, summary, date_label, order in INSIGHT_PUBLICATIONS:
        InsightPublication.objects.update_or_create(
            title=title,
            defaults={
                "category_label": category_label, "summary": summary, "date_label": date_label,
                "order": order, "published": True,
            },
        )

    for name, address, maps_url, order in OFFICE_LOCATIONS:
        OfficeLocation.objects.update_or_create(
            name=name, defaults={"address": address, "maps_url": maps_url, "order": order, "published": True},
        )

    for page, title, meta_description in PAGE_SEO:
        PageSEO.objects.update_or_create(
            page=page, defaults={"title": title, "meta_description": meta_description},
        )


def unseed(apps, schema_editor):
    apps.get_model("corporate", "SiteSettings").objects.filter(pk=1).delete()
    apps.get_model("corporate", "NavLink").objects.filter(label__in=[n[0] for n in NAV_LINKS]).delete()
    apps.get_model("corporate", "SocialLink").objects.filter(label__in=[s[0] for s in SOCIAL_LINKS]).delete()
    apps.get_model("corporate", "HeroSlide").objects.filter(headline__in=[h[0] for h in HERO_SLIDES]).delete()
    apps.get_model("corporate", "ServiceCard").objects.filter(title__in=[s[0] for s in SERVICE_CARDS]).delete()
    apps.get_model("corporate", "PartnerCard").objects.filter(name__in=[p[0] for p in PARTNER_CARDS]).delete()
    apps.get_model("corporate", "VisionPillar").objects.filter(title__in=[v[0] for v in VISION_PILLARS]).delete()
    apps.get_model("corporate", "AboutCard").objects.filter(title__in=[a[1] for a in ABOUT_CARDS]).delete()
    apps.get_model("corporate", "InsightPublication").objects.filter(title__in=[i[1] for i in INSIGHT_PUBLICATIONS]).delete()
    apps.get_model("corporate", "OfficeLocation").objects.filter(name__in=[o[0] for o in OFFICE_LOCATIONS]).delete()
    apps.get_model("corporate", "PageSEO").objects.filter(page__in=[p[0] for p in PAGE_SEO]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("corporate", "0004_add_cms_models"),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
