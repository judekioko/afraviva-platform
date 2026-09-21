from datetime import timedelta

from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone


class AdminCSPMiddleware:
    """The rest of the site deliberately uses Alpine's CSP-safe build (see
    static/vendor/alpine.min.js) so the strict `script-src 'self'` policy
    holds everywhere public. django-unfold's admin theme bundles the regular
    Alpine build instead, which needs 'unsafe-eval' to evaluate its x-data
    expressions. Rather than weaken CSP site-wide for that, this widens
    script-src only for /admin/ responses — already gated behind login (and
    optionally 2FA), not the public surface the strict policy protects.

    Must sit BEFORE CSPMiddleware in MIDDLEWARE so this runs after it on the
    way out (Django's response phase runs middleware bottom-up).
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        header = response.get("Content-Security-Policy")
        if request.path.startswith("/admin/") and header:
            response["Content-Security-Policy"] = header.replace(
                "script-src 'self'", "script-src 'self' 'unsafe-eval'",
            )
        return response

PASSWORD_MAX_AGE_DAYS = 90

# Paths a staff member with an expired/unset password must still be able to
# reach — otherwise they could never get to the page that lets them fix it.
_EXEMPT_PATH_PREFIXES = (
    "/accounts/",
    "/admin/logout/",
    "/static/",
)


class PasswordExpiryMiddleware:
    """Forces approved staff (is_staff, not superuser) to set/refresh their
    password every PASSWORD_MAX_AGE_DAYS. Superusers are exempt — this exists
    for the staff-invite flow, not to risk locking out the account that
    manages everyone else's access.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, "user", None)
        if (
            user is not None
            and user.is_authenticated
            and user.is_staff
            and not user.is_superuser
            and not request.path.startswith(_EXEMPT_PATH_PREFIXES)
        ):
            profile = getattr(user, "staff_profile", None)
            changed_at = profile.password_changed_at if profile else None
            expired = changed_at is None or (timezone.now() - changed_at) > timedelta(days=PASSWORD_MAX_AGE_DAYS)
            if expired:
                return redirect(reverse("accounts:password_change"))
        return self.get_response(request)
