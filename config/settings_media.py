"""Settings for the media.afraviva.com / afravivamedia.com Passenger app.
Same codebase and database as the main site — only the URLconf differs, so
these two domains serve Media hub content at their root instead of /media/.
afravivamedia.com is the main address; media.afraviva.com redirects to it.
"""

from .settings import *  # noqa: F401,F403

ROOT_URLCONF = "config.urls_media"

MIDDLEWARE = ["media_hub.middleware.redirect_to_main_media_domain"] + MIDDLEWARE  # noqa: F405
