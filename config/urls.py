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
    path("", include("corporate.urls")),
]

# Uploaded images (team photos here; media/farm cover images on their own
# subdomains via urls_media.py/urls_farms.py) — served directly rather than
# gated behind DEBUG, since there's no separate static-file server in front
# of this small deployment.
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
