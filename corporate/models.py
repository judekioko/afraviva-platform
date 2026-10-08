from django.db import models

from .validators import validate_document_upload, validate_image_upload


class FAQItem(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0)
    published = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.question


class TeamMember(models.Model):
    name = models.CharField(max_length=120)
    role = models.CharField(max_length=120)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to="team/", blank=True, null=True, validators=[validate_image_upload])
    order = models.PositiveIntegerField(default=0)
    published = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.name} ({self.role})"


class SiteSettings(models.Model):
    """Sitewide text/links editable from the admin. Singleton — always fetch
    it via SiteSettings.load(), never SiteSettings.objects.get(...).
    """

    # Header / footer
    whatsapp_number = models.CharField(
        max_length=32, default="+254705837629",
        help_text="Include the country code, no spaces or dashes, e.g. +254705837629.",
    )
    whatsapp_message = models.CharField(
        max_length=255, blank=True, default="Hello I would like to connect",
        help_text="Pre-filled message when someone taps the WhatsApp button.",
    )
    contact_email = models.EmailField(default="Admin@afraviva.com")
    contact_phone_lines = models.TextField(
        default="Kenya: +254 705 837629\nUganda: +256 392 964978",
        help_text="One phone line per row, e.g. \"Kenya: +254 700 000000\".",
    )
    footer_blurb = models.TextField(
        default="Media, Homes and Farms — brands of AfricaNext Opportunities (ANO), "
        "building sustainable, purpose-driven businesses across Africa.",
    )
    copyright_text = models.CharField(
        max_length=255,
        default="AfraViva, a brand of AfricaNext Opportunities. All rights reserved. · Site developed by Jude Kioko",
        help_text="Shown after the year in the footer, e.g. \"(c) 2026 {this text}\".",
    )
    homes_url = models.URLField(default="https://homes.afraviva.com")
    media_url = models.URLField(default="https://afravivamedia.com")
    farms_url = models.URLField(default="https://farms.afraviva.com")

    # Homepage
    home_intro_heading = models.CharField(
        max_length=200, default="Building Africa's Future with Purpose and Impact",
    )
    home_intro_body = models.TextField(
        default="At AfraViva, the brand of AfricaNext Opportunities (ANO), we blend talent and ambition to grow "
        "impactful businesses across Africa. Rooted in Christian values of justice and community, we "
        "accelerate startups and invest in sectors that uplift lives — delivering sustainability and success.",
    )
    home_media_partner_name = models.CharField(max_length=120, blank=True, default="LifeSiteNews")
    home_media_partner_description = models.TextField(
        blank=True,
        default="Internet news service established in Canada in 1997, now active worldwide, dedicated to "
        "issues of life, family, and faith.",
    )
    vision_eyebrow = models.CharField(
        max_length=200, blank=True, default="AfricaNext Vision, Guiding Principles & Objectives",
    )
    vision_heading = models.CharField(max_length=200, blank=True, default="Crafting a future of innovation and impact")
    vision_fun_fact = models.TextField(
        blank=True,
        default="AfricaNext's vision is guided by time-tested Christian values as elucidated in sacred scripture, "
        "as well as classic Church social teachings such as Pope Leo XIII's \"Of New Things\" "
        "(Rerum Novarum, 1891) and Pope John Paul II's \"Through Work\" (Laborem Exercens, 1981).",
    )

    # Services page (and the homepage services section, which shares this copy)
    services_intro = models.TextField(
        blank=True, default="Discover how we empower your goals with innovative expertise.",
    )

    # ThrivePoint Insights page
    thrivepoint_intro = models.TextField(
        blank=True,
        default="Full report content and downloads will be added once migrated from the current site.",
    )

    # About page
    about_hero_heading = models.CharField(max_length=200, blank=True, default="We are committed to excellence")
    about_hero_body = models.TextField(
        blank=True,
        default="We believe in the power of sustainable practices, spiritual values and cultural richness "
        "to create a brighter future for Africa.",
    )
    about_overview = models.TextField(
        blank=True,
        default="We work with ambitious clients across Africa who want to define the future, not hide from it.\n\n"
        "Our firm delivers innovative solutions in Agribusiness, Digital Media Production, Estate "
        "Development Consultancy, and Business Development. We partner with individuals, organizations "
        "and institutions to drive progress, spark growth, and unlock new opportunities across diverse "
        "sectors and communities.\n\n"
        "We measure our success by the positive impact we create: empowering farmers and agribusinesses, "
        "crafting compelling digital content, guiding estate investments with expert insight, and building "
        "sustainable businesses that thrive in today's competitive landscape.",
        help_text="Separate paragraphs with a blank line.",
    )
    about_mission = models.TextField(
        blank=True,
        default="We craft transformative, client-centric solutions to reshape industries and enrich lives. "
        "Guided by integrity, innovation, and an intimate knowledge of Africa's vibrant landscape, "
        "we forge a path to a thriving, prosperous future.",
    )
    about_footnote = models.TextField(
        blank=True,
        default="AfraViva is the operating brand of AfricaNext Opportunities (ANO), guided by time-tested "
        "Christian values of justice and community.",
    )

    class Meta:
        verbose_name = "Site settings"
        verbose_name_plural = "Site settings"

    def __str__(self):
        return "Site settings"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    @property
    def whatsapp_url(self):
        from urllib.parse import quote

        number = self.whatsapp_number.replace(" ", "").lstrip("+")
        return f"https://wa.me/{number}?text={quote(self.whatsapp_message)}"


class NavLink(models.Model):
    PAGE_CHOICES = [
        ("home", "Home"),
        ("about", "About"),
        ("services", "Services"),
        ("thrivepoint", "ThrivePoint Insights"),
        ("faq", "FAQ"),
        ("contact", "Contact"),
    ]
    label = models.CharField(max_length=60)
    page = models.CharField(
        max_length=20, choices=PAGE_CHOICES, blank=True,
        help_text="Pick a page on this site — or leave blank and fill in an external link below "
        "(for Media, Farms, Homes, or anywhere off this site).",
    )
    external_url = models.URLField(blank=True, help_text="Used only when 'page' above is left blank.")
    order = models.PositiveIntegerField(default=0)
    published = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.label


class SocialLink(models.Model):
    label = models.CharField(max_length=40, help_text="e.g. Facebook, Instagram, YouTube")
    url = models.URLField()
    order = models.PositiveIntegerField(default=0)
    published = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.label


class HeroSlide(models.Model):
    """Rotating headline/subhead shown in the homepage hero banner."""

    headline = models.CharField(max_length=200)
    subhead = models.CharField(max_length=300, blank=True)
    order = models.PositiveIntegerField(default=0)
    published = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.headline


class ServiceCard(models.Model):
    """A service offering card — shown on both the homepage and the Services
    page, which share this same list so the two pages can't drift apart.
    """

    title = models.CharField(max_length=120)
    description = models.TextField()
    link_label = models.CharField(max_length=60, blank=True, default="Learn more →")
    link_url = models.CharField(
        max_length=255, blank=True,
        help_text="A full link (https://...) or a path on this site (e.g. /contact/). Leave blank to hide the link.",
    )
    order = models.PositiveIntegerField(default=0)
    published = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class PartnerCard(models.Model):
    """A partner/success-story card — shown on both the homepage and the
    Services page, which share this same list.
    """

    name = models.CharField(max_length=120)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)
    published = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.name


class VisionPillar(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)
    published = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class AboutCard(models.Model):
    SECTION_MISSION = "mission"
    SECTION_DIFFERENT = "different"
    SECTION_CHOICES = [
        (SECTION_MISSION, "Our mission — focus areas"),
        (SECTION_DIFFERENT, "What makes us different"),
    ]
    section = models.CharField(max_length=20, choices=SECTION_CHOICES)
    title = models.CharField(max_length=120)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)
    published = models.BooleanField(default=True)

    class Meta:
        ordering = ["section", "order", "id"]

    def __str__(self):
        return f"{self.title} ({self.get_section_display()})"


class InsightPublication(models.Model):
    """A ThrivePoint Insights report/guide — shown as a teaser on the
    homepage and in full on the ThrivePoint Insights page.
    """

    category_label = models.CharField(max_length=40, blank=True, help_text="e.g. Report, Guide, Trends")
    title = models.CharField(max_length=200)
    summary = models.TextField()
    date_label = models.CharField(max_length=40, blank=True, help_text="e.g. 2025")
    file = models.FileField(
        upload_to="thrivepoint/", blank=True, null=True, validators=[validate_document_upload],
        help_text="Optional PDF or document for readers to download.",
    )
    external_url = models.URLField(blank=True, help_text="Optional link instead of, or alongside, a file.")
    order = models.PositiveIntegerField(default=0)
    published = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class OfficeLocation(models.Model):
    name = models.CharField(max_length=80, help_text="e.g. Nairobi HQ")
    address = models.TextField()
    maps_url = models.URLField(blank=True, help_text="Optional Google Maps link.")
    order = models.PositiveIntegerField(default=0)
    published = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.name


class PageSEO(models.Model):
    PAGE_CHOICES = [
        ("home", "Home"),
        ("about", "About"),
        ("services", "Services"),
        ("thrivepoint", "ThrivePoint Insights"),
        ("faq", "FAQ"),
        ("contact", "Contact"),
        ("media_list", "Media — list page"),
        ("farms_list", "Farms — list page"),
    ]
    page = models.CharField(max_length=20, choices=PAGE_CHOICES, unique=True)
    title = models.CharField(max_length=200, blank=True, help_text="Browser tab title. Leave blank to use the default.")
    meta_description = models.CharField(
        max_length=300, blank=True, help_text="Search engine snippet. Leave blank to use the default.",
    )

    def __str__(self):
        return self.get_page_display()
