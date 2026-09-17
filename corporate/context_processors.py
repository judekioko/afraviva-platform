from django.conf import settings


def admin_idle_timeout(request):
    return {"ADMIN_IDLE_TIMEOUT_SECONDS": settings.ADMIN_IDLE_TIMEOUT_SECONDS}


def site_nav(request):
    """Global nav config, shared across every template.

    homes.afraviva.com is a separate, already-built site — always an
    external link here, never a Django URL, so it can't accidentally
    be pointed at anything in this project.
    """
    return {
        "NAV_LINKS": [
            {"label": "Home", "url": "corporate:home"},
            {"label": "About", "url": "corporate:about"},
            {"label": "Services", "url": "corporate:services"},
            {"label": "Media", "url": "media_hub:list"},
            {"label": "Farms", "url": "farms_hub:list"},
            {"label": "ThrivePoint Insights", "url": "corporate:thrivepoint"},
            {"label": "FAQ", "url": "corporate:faq"},
            {"label": "Contact", "url": "corporate:contact"},
        ],
        "HOMES_URL": "https://homes.afraviva.com",
        "MEDIA_SOCIAL_LINKS": [
            {"label": "Facebook", "url": "https://www.facebook.com/share/14iSWn76ZEr/"},
            {"label": "Instagram", "url": "https://www.instagram.com/afraviva_media"},
            {"label": "TikTok", "url": "https://www.tiktok.com/@afravivamedia"},
            {"label": "YouTube", "url": "https://www.youtube.com/@AfravivaMedia"},
            {"label": "X", "url": "https://x.com/AfravivaMedia"},
        ],
    }
