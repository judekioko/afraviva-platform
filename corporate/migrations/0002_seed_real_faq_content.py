# Loads AfraViva's real FAQ copy, migrated from afraviva.com/faq.php.

from django.db import migrations

FAQS = [
    (
        "How do your Nairobi and Kampala offices support clients?",
        "Our Nairobi office serves as the headquarters, handling strategic planning and major "
        "projects, while Kampala focuses on regional support, offering localized services in "
        "agribusiness, Airbnb management, digital media, and business development to meet East "
        "African needs.",
    ),
    (
        "What agribusiness solutions do you offer in Kenya and Uganda?",
        "We provide farm-to-market solutions, including supply chain optimization, digital "
        "platforms for farmers, and training programs in Nairobi and Kampala, tailored to boost "
        "productivity and sustainability in East African agriculture.",
    ),
    (
        "How do you help manage or promote Airbnb properties?",
        "Our Homes Airbnb service includes property listing management, professional "
        "photography, pricing strategies, and guest communication, designed to maximize bookings "
        "in popular destinations like Nairobi and Kampala.",
    ),
    (
        "What digital media and production services are available?",
        "We offer video production, social media campaigns, and content creation in Kenya and "
        "Uganda, helping brands tell their stories through high-quality media tailored to local "
        "audiences, from Nairobi's urban markets to Kampala's vibrant communities.",
    ),
    (
        "How do you support business development in the region?",
        "Our business development services include market entry strategies, partnership "
        "facilitation, and growth planning, with teams in Nairobi and Kampala guiding businesses "
        "to thrive in Kenya's tech hubs and Uganda's emerging markets.",
    ),
]


def seed_faqs(apps, schema_editor):
    FAQItem = apps.get_model("corporate", "FAQItem")
    for order, (question, answer) in enumerate(FAQS):
        FAQItem.objects.update_or_create(
            question=question, defaults={"answer": answer, "order": order, "published": True}
        )


def remove_faqs(apps, schema_editor):
    FAQItem = apps.get_model("corporate", "FAQItem")
    FAQItem.objects.filter(question__in=[q for q, _ in FAQS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("corporate", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_faqs, remove_faqs),
    ]
