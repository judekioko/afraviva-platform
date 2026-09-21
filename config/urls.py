from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import RedirectView
from django.views.static import serve

if settings.ADMIN_REQUIRE_2FA:
    # Retrofits the default admin.site to also require a verified OTP device —
    # the officially documented django-otp integration for the built-in
    # AdminSite. Gated behind a flag (default off) so this can't be flipped on
    # by an env change alone before every staff account has enrolled a device;
    # enrolling one is already possible today under the TOTP devices admin page.
    from django_otp.admin import OTPAdminSite

    admin.site.__class__ = OTPAdminSite

urlpatterns = [
    # Bare name (not namespaced under admin/accounts) so django-unfold's own
    # login template picks it up automatically for its "Forgotten your
    # password?" link — see venv .../unfold/templates/admin/login.html.
    path(
        "admin/password_reset/",
        RedirectView.as_view(pattern_name="accounts:password_reset", permanent=False),
        name="admin_password_reset",
    ),
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("enquiries/", include("enquiries.urls")),
    path("", include("corporate.urls")),
]

# Uploaded images (team photos here; media/farm cover images on their own
# subdomains via urls_media.py/urls_farms.py). django.conf.urls.static.static()
# is a no-op when DEBUG=False, so it never actually served anything in
# production — use django.views.static.serve directly instead, since there's
# no separate static-file server in front of this small deployment.
urlpatterns += [
    re_path(
        r"^%s(?P<path>.*)$" % settings.MEDIA_URL.lstrip("/"),
        serve,
        {"document_root": settings.MEDIA_ROOT},
    ),
]
