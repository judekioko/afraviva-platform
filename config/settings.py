"""
Django settings for the AfraViva platform (Corporate + Media + Farms).
homes.afraviva.com is a separate, already-built site and is not part of this project.
"""

from pathlib import Path
import environ
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    DEBUG=(bool, False),
)
environ.Env.read_env(BASE_DIR / ".env")

DEBUG = env("DEBUG")

_INSECURE_DEFAULT_KEY = "django-insecure-local-dev-only-change-in-prod"
SECRET_KEY = env("SECRET_KEY", default=_INSECURE_DEFAULT_KEY)
if not DEBUG and SECRET_KEY == _INSECURE_DEFAULT_KEY:
    # Never let the well-known dev key run in production — fail loudly instead
    # of silently serving with a secret an attacker can read straight off GitHub.
    raise ImproperlyConfigured(
        "SECRET_KEY is not set. Set a real SECRET_KEY in the environment/.env before running with DEBUG=False."
    )

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["localhost", "127.0.0.1"])

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_otp",
    "django_otp.plugins.otp_totp",
    "axes",
    "corporate",
    "media_hub",
    "farms_hub",
    "enquiries",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # serves /static/ with DEBUG=False, no separate web-server config needed
    "csp.middleware.CSPMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django_otp.middleware.OTPMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "axes.middleware.AxesMiddleware",  # must stay last
]

# django-axes: lock out repeated failed logins on /admin/login/ (and any other
# auth form). AxesStandaloneBackend must come first so it can veto a login
# before ModelBackend even checks the password.
AUTHENTICATION_BACKENDS = [
    "axes.backends.AxesStandaloneBackend",
    "django.contrib.auth.backends.ModelBackend",
]
AXES_FAILURE_LIMIT = 5
AXES_COOLOFF_TIME = 1  # hour
AXES_LOCKOUT_PARAMETERS = ["username", "ip_address"]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "corporate.context_processors.site_nav",
                "corporate.context_processors.admin_idle_timeout",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Database
# Local dev defaults to SQLite so no MySQL server is needed on this machine.
# Production (Truehost) sets DATABASE_URL to a mysql:// URL, which pulls in
# mysqlclient there (Linux host, no Windows build issues).
_database_url = env("DATABASE_URL", default="") or f"sqlite:///{BASE_DIR / 'db.sqlite3'}"
DATABASES = {"default": env.db_url_config(_database_url)}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Africa/Nairobi"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    # The manifest variant requires a collectstatic run to exist (it looks up
    # hashed filenames from staticfiles.json) — fine in production, where
    # passenger_wsgi.py always runs collectstatic at startup, but it breaks
    # local dev/tests with no build step. Plain WhiteNoiseStorage still gets
    # served correctly by the middleware either way.
    "staticfiles": {
        "BACKEND": (
            "whitenoise.storage.CompressedManifestStaticFilesStorage"
            if not DEBUG
            else "django.contrib.staticfiles.storage.StaticFilesStorage"
        )
    },
}

MEDIA_URL = "uploads/"
MEDIA_ROOT = BASE_DIR / "mediafiles"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- Security (Rebuild Plan §6) ---
CONTENT_SECURITY_POLICY = {
    "DIRECTIVES": {
        "default-src": ["'self'"],
        "img-src": ["'self'", "data:"],
        "style-src": ["'self'", "'unsafe-inline'", "https://fonts.googleapis.com"],
        "font-src": ["'self'", "https://fonts.gstatic.com"],
        "script-src": ["'self'"],
        "frame-ancestors": ["'none'"],
    },
}
X_FRAME_OPTIONS = "DENY"
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_REFERRER_POLICY = "same-origin"

# Cookie hardening. SameSite=Lax on both is Django's own default — made explicit
# here so it can't drift if that default ever changes. CSRF_COOKIE_HTTPONLY is
# safe to force on: nothing in this codebase reads the CSRF cookie from JS, the
# token travels via the {% csrf_token %} hidden input HTMX submits with the form.
SESSION_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_HTTPONLY = True

if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    # This only adds "preload" to the header Django sends — it does not submit
    # the domain to the browser preload list. That's a separate, deliberate,
    # slow-to-reverse step at hstspreload.org, left for AfraViva to do once
    # every subdomain is confirmed fully HTTPS-ready.
    SECURE_HSTS_PRELOAD = True

# Off by default: flipping this to True makes the admin require a confirmed
# TOTP device (django_otp), on top of username/password. Turn it on only after
# every current staff account has enrolled a device under Admin > TOTP devices
# — enabling it first would lock out anyone without one, with no self-recovery.
ADMIN_REQUIRE_2FA = env.bool("ADMIN_REQUIRE_2FA", default=False)

# Auto-logout staff/admin sessions after inactivity, like a banking system.
# SESSION_SAVE_EVERY_REQUEST makes the expiry a sliding window from the last
# request, so it's genuinely "minutes of inactivity", not minutes since login.
# The admin page also runs a client-side idle timer (static/js/admin-idle-timeout.js)
# so an unattended tab gets kicked to the login page instead of just erroring
# on the next click — keep ADMIN_IDLE_TIMEOUT_SECONDS in sync with that in mind.
ADMIN_IDLE_TIMEOUT_SECONDS = env.int("ADMIN_IDLE_TIMEOUT_SECONDS", default=900)
SESSION_COOKIE_AGE = ADMIN_IDLE_TIMEOUT_SECONDS
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# --- Email (contact form -> Truehost SMTP for @afraviva.com mailboxes) ---
EMAIL_BACKEND = env("EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend")
EMAIL_HOST = env("EMAIL_HOST", default="")
EMAIL_PORT = env.int("EMAIL_PORT", default=587)
EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="")
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS", default=True)
ENQUIRY_NOTIFY_TO = env.list("ENQUIRY_NOTIFY_TO", default=["kiokoitdev@afraviva.com"])

# Was pointed at a "/staff/login/" that was never built. Nothing in this project
# uses @login_required/LoginRequiredMixin today, but keep this correct rather
# than dangling in case a future staff-only view (non-admin) needs it.
LOGIN_URL = "/admin/login/"
