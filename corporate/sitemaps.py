from django.contrib.sitemaps import Sitemap
from django.http import HttpResponse
from django.urls import reverse
from django.views.decorators.http import require_GET


class CorporateSitemap(Sitemap):
    protocol = "https"
    changefreq = "monthly"

    def items(self):
        return ["home", "about", "services", "thrivepoint", "faq", "contact"]

    def location(self, item):
        return reverse(f"corporate:{item}")


@require_GET
def robots_txt(request):
    """Served at /robots.txt on every domain; points crawlers at that
    domain's own /sitemap.xml."""
    lines = [
        "User-agent: *",
        "Disallow: /admin/",
        "Disallow: /accounts/",
        f"Sitemap: {request.build_absolute_uri('/sitemap.xml')}",
    ]
    return HttpResponse("\n".join(lines) + "\n", content_type="text/plain")
