"""Root URLconf for farms.afraviva.com — serves the Farms hub content
mounted at the domain root instead of /farms/.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

urlpatterns = [
    path("", include("farms_hub.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
