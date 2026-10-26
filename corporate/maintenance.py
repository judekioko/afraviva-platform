"""Maintenance mode for afraviva.com, the Media sites and Farms.

While a file named `maintenance` exists in the app's tmp/ folder
(~/afraviva-platform/tmp/maintenance on the server), every public page
answers 503 with a "back soon" page and a Retry-After header, so search
engines treat the outage as temporary. All four apps share that folder, so
one file switches them all. Staff admin, login pages, static files and
uploads keep working. Create or delete the file in cPanel File Manager; no
restart is needed.
"""

from pathlib import Path

from django.conf import settings
from django.template.loader import render_to_string
from django.http import HttpResponse

FLAG = Path(settings.BASE_DIR) / "tmp" / "maintenance"
ALWAYS_OPEN = ("/admin", "/accounts/", "/static/", "/" + settings.MEDIA_URL.lstrip("/"))


def maintenance_mode(get_response):
    def middleware(request):
        if FLAG.exists() and not request.path.startswith(ALWAYS_OPEN):
            response = HttpResponse(render_to_string("maintenance.html"), status=503)
            response["Retry-After"] = "3600"
            response["Cache-Control"] = "no-store"
            return response
        return get_response(request)

    return middleware
