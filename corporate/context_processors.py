from django.conf import settings


def admin_idle_timeout(request):
    return {"ADMIN_IDLE_TIMEOUT_SECONDS": settings.ADMIN_IDLE_TIMEOUT_SECONDS}


# Only these three hosts render without the corporate app in their urlconf
# (see config/urls_media.py / config/urls_farms.py) — everything else,
# including afraviva.com itself and local dev (localhost/127.0.0.1), is
# treated as the main site so corporate: URLs resolve normally there.
SUBDOMAIN_HOSTS = {"media.afraviva.com", "farms.afraviva.com", "afravivamedia.com"}
CORPORATE_SITE_URL = "https://afraviva.com"

# path, not Django url name — these need to work even when rendered from a
# request whose urlconf doesn't include the corporate app at all (every
# subdomain except afraviva.com itself).
_CORPORATE_PATHS = {
    "home": "/",
    "about": "/about/",
    "services": "/services/",
    "thrivepoint": "/thrivepoint-insights/",
    "faq": "/faq/",
    "contact": "/contact/",
}


def site_nav(request):
    """Global nav config, shared across every template — including the
    Media hub and Farms hub, which now live on their own subdomains
    (media.afraviva.com, afravivamedia.com, farms.afraviva.com) with their
    own urlconf that doesn't include the corporate app's URLs at all.

    On afraviva.com itself, corporate links resolve normally with
    {% url %}. Everywhere else, they — and the "Home" logo link — become
    plain absolute links back to afraviva.com, via the "external" key
    NAV_LINKS already supports (the same pattern Homes/Media/Farms use from
    the main site).
    """
    on_main_site = request.get_host().split(":")[0] not in SUBDOMAIN_HOSTS

    def corp_link(label, name):
        if on_main_site:
            return {"label": label, "url": f"corporate:{name}"}
        return {"label": label, "external": CORPORATE_SITE_URL + _CORPORATE_PATHS[name]}

    return {
        "NAV_LINKS": [
            corp_link("Home", "home"),
            corp_link("About", "about"),
            corp_link("Services", "services"),
            {"label": "Media", "external": "https://media.afraviva.com"},
            {"label": "Farms", "external": "https://farms.afraviva.com"},
            corp_link("ThrivePoint Insights", "thrivepoint"),
            corp_link("FAQ", "faq"),
            corp_link("Contact", "contact"),
        ],
        "ON_MAIN_SITE": on_main_site,
        "HOME_HREF": CORPORATE_SITE_URL + "/",
        "HOMES_URL": "https://homes.afraviva.com",
        "MEDIA_SITE_URL": "https://media.afraviva.com",
        "FARMS_SITE_URL": "https://farms.afraviva.com",
        "MEDIA_SOCIAL_LINKS": [
            {"label": "Facebook", "url": "https://www.facebook.com/share/14iSWn76ZEr/"},
            {"label": "Instagram", "url": "https://www.instagram.com/afraviva_media"},
            {"label": "TikTok", "url": "https://www.tiktok.com/@afravivamedia"},
            {"label": "YouTube", "url": "https://www.youtube.com/@AfravivaMedia"},
            {"label": "X", "url": "https://x.com/AfravivaMedia"},
        ],
    }
