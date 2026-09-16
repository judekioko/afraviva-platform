from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("enquiries/", include("enquiries.urls")),
    path("media/", include("media_hub.urls")),
    path("farms/", include("farms_hub.urls")),
    path("", include("corporate.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
