"""Root URLconf for farms.afraviva.com — serves the Farms hub content
mounted at the domain root instead of /farms/.
"""

from django.conf import settings
from django.urls import include, path, re_path
from django.views.static import serve

urlpatterns = [
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
