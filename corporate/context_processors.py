from django.conf import settings

from .models import NavLink, OfficeLocation, PageSEO, SiteSettings, SocialLink


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
    """Global nav config + sitewide settings, shared across every template —
    including the Media hub and Farms hub, which now live on their own
    subdomains (media.afraviva.com, afravivamedia.com, farms.afraviva.com)
    with their own urlconf that doesn't include the corporate app's URLs at
    all.

    On afraviva.com itself, corporate links resolve normally with
    {% url %}. Everywhere else, they become plain absolute links back to
    afraviva.com, via NavLink.external_url — the same pattern Media/Farms/
    Homes links already use.

    Nav links, social links, office details and the rest of the sitewide
    copy below all come from the admin (see corporate/models.py) instead of
    being hardcoded, so non-technical staff can edit them without touching code.
    """
    on_main_site = request.get_host().split(":")[0] not in SUBDOMAIN_HOSTS
    site = SiteSettings.load()

    def resolve_link(link):
        if link.page:
            if on_main_site:
                return {"label": link.label, "url": f"corporate:{link.page}"}
            return {"label": link.label, "external": CORPORATE_SITE_URL + _CORPORATE_PATHS[link.page]}
        return {"label": link.label, "external": link.external_url}

    return {
        "NAV_LINKS": [resolve_link(link) for link in NavLink.objects.filter(published=True)],
        "ON_MAIN_SITE": on_main_site,
        "HOME_HREF": CORPORATE_SITE_URL + "/",
        "HOMES_URL": site.homes_url,
        "MEDIA_SITE_URL": site.media_url,
        "FARMS_SITE_URL": site.farms_url,
        "MEDIA_SOCIAL_LINKS": SocialLink.objects.filter(published=True),
        "SITE": site,
        "OFFICE_LOCATIONS": OfficeLocation.objects.filter(published=True),
        "PAGE_SEO": {seo.page: seo for seo in PageSEO.objects.all()},
    }
