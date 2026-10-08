"""Root URLconf for farms.afraviva.com — serves the Farms hub content
mounted at the domain root instead of /farms/.
"""

from django.conf import settings
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path, re_path
from django.views.static import serve

from corporate.sitemaps import robots_txt
from farms_hub.sitemaps import FarmsSitemap

urlpatterns = [
    path("sitemap.xml", sitemap, {"sitemaps": {"posts": FarmsSitemap}}, name="sitemap"),
    path("robots.txt", robots_txt),
    path("", include("farms_hub.urls")),
]

# django.conf.urls.static.static() is a no-op when DEBUG=False, so it never
# actually served anything in production — use django.views.static.serve
# directly instead.
urlpatterns += [
    re_path(
        r"^%s(?P<path>.*)$" % settings.MEDIA_URL.lstrip("/"),
        serve,
        {"document_root": settings.MEDIA_ROOT},
    ),
]
