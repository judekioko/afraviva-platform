from django.contrib import admin

from .models import (
    AboutCard,
    FAQItem,
    HeroSlide,
    InsightPublication,
    NavLink,
    OfficeLocation,
    PageSEO,
    PartnerCard,
    ServiceCard,
    SiteSettings,
    SocialLink,
    TeamMember,
    VisionPillar,
)

admin.site.site_header = "AfraViva Admin"
admin.site.site_title = "AfraViva Admin"
admin.site.index_title = "AfraViva content management"


@admin.register(FAQItem)
class FAQItemAdmin(admin.ModelAdmin):
    list_display = ("question", "order", "published")
    list_editable = ("order", "published")


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ("name", "role", "order", "published")
    list_editable = ("order", "published")


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Header, footer & contact", {
            "fields": (
                "whatsapp_number", "whatsapp_message",
                "contact_email", "contact_phone_lines",
                "footer_blurb", "copyright_text",
                "homes_url", "media_url", "farms_url",
            ),
        }),
        ("Homepage", {
            "fields": (
                "home_intro_heading", "home_intro_body",
                "home_media_partner_name", "home_media_partner_description",
                "vision_eyebrow", "vision_heading", "vision_fun_fact",
            ),
        }),
        ("Services page", {"fields": ("services_intro",)}),
        ("ThrivePoint Insights page", {"fields": ("thrivepoint_intro",)}),
        ("About page", {
            "fields": (
                "about_hero_heading", "about_hero_body",
                "about_overview", "about_mission", "about_footnote",
            ),
        }),
    )

    def has_add_permission(self, request):
        # Singleton — one row only, always editable, never deletable.
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        # Skip the list page entirely and go straight to the (only) row.
        from django.shortcuts import redirect

        obj = SiteSettings.load()
        return redirect("admin:corporate_sitesettings_change", obj.pk)


@admin.register(NavLink)
class NavLinkAdmin(admin.ModelAdmin):
    list_display = ("label", "page", "external_url", "order", "published")
    list_editable = ("order", "published")


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ("label", "url", "order", "published")
    list_editable = ("order", "published")


@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display = ("headline", "order", "published")
    list_editable = ("order", "published")


@admin.register(ServiceCard)
class ServiceCardAdmin(admin.ModelAdmin):
    list_display = ("title", "order", "published")
    list_editable = ("order", "published")


@admin.register(PartnerCard)
class PartnerCardAdmin(admin.ModelAdmin):
    list_display = ("name", "order", "published")
    list_editable = ("order", "published")


@admin.register(VisionPillar)
class VisionPillarAdmin(admin.ModelAdmin):
    list_display = ("title", "order", "published")
    list_editable = ("order", "published")


@admin.register(AboutCard)
class AboutCardAdmin(admin.ModelAdmin):
    list_display = ("title", "section", "order", "published")
    list_filter = ("section",)
    list_editable = ("order", "published")


@admin.register(InsightPublication)
class InsightPublicationAdmin(admin.ModelAdmin):
    list_display = ("title", "category_label", "date_label", "order", "published")
    list_editable = ("order", "published")


@admin.register(OfficeLocation)
class OfficeLocationAdmin(admin.ModelAdmin):
    list_display = ("name", "order", "published")
    list_editable = ("order", "published")


@admin.register(PageSEO)
class PageSEOAdmin(admin.ModelAdmin):
    list_display = ("page", "title", "meta_description")
