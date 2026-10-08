"""Root URLconf for media.afraviva.com and afravivamedia.com — both serve
the same Media hub content, mounted at the domain root instead of /media/.
"""

from django.conf import settings
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path, re_path
from django.views.static import serve

from corporate.sitemaps import robots_txt
from media_hub.sitemaps import MediaSitemap

urlpatterns = [
    path("sitemap.xml", sitemap, {"sitemaps": {"posts": MediaSitemap}}, name="sitemap"),
    path("robots.txt", robots_txt),
    path("", include("media_hub.urls")),
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
