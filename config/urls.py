from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

if settings.ADMIN_REQUIRE_2FA:
    # Retrofits the default admin.site to also require a verified OTP device —
    # the officially documented django-otp integration for the built-in
    # AdminSite. Gated behind a flag (default off) so this can't be flipped on
    # by an env change alone before every staff account has enrolled a device;
    # enrolling one is already possible today under the TOTP devices admin page.
    from django_otp.admin import OTPAdminSite

    admin.site.__class__ = OTPAdminSite

urlpatterns = [
    path("admin/", admin.site.urls),
    path("enquiries/", include("enquiries.urls")),
    path("media/", include("media_hub.urls")),
    path("farms/", include("farms_hub.urls")),
    path("", include("corporate.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
