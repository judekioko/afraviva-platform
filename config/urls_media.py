"""Root URLconf for media.afraviva.com and afravivamedia.com — both serve
the same Media hub content, mounted at the domain root instead of /media/.
"""

from django.conf import settings
from django.urls import include, path, re_path
from django.views.static import serve

urlpatterns = [
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
