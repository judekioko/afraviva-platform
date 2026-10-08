from django.http import HttpResponsePermanentRedirect

MAIN_MEDIA_DOMAIN = "afravivamedia.com"
OLD_MEDIA_DOMAIN = "media.afraviva.com"


def redirect_to_main_media_domain(get_response):
    """301 every media.afraviva.com request to the same path on
    afravivamedia.com, so search engines index one copy of each Media page.
    """

    def middleware(request):
        host = request.META.get("HTTP_HOST", "").split(":")[0].lower()
        if host == OLD_MEDIA_DOMAIN:
            return HttpResponsePermanentRedirect(f"https://{MAIN_MEDIA_DOMAIN}{request.get_full_path()}")
        return get_response(request)

    return middleware
