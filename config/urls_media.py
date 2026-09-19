"""Root URLconf for media.afraviva.com and afravivamedia.com — both serve
the same Media hub content, mounted at the domain root instead of /media/.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

urlpatterns = [
    path("", include("media_hub.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
