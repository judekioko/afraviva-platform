"""schema.org JSON-LD for search engines: who AfraViva is (Organization, on
every page) and what each Media/Farms post is (Article). Built in Python so
the JSON is always valid, whatever text editors type into the admin.
"""

import json

from django import template
from django.templatetags.static import static
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe
from django.utils.text import Truncator

register = template.Library()

MAIN_SITE = "https://afraviva.com"


def _organization(context):
    org = {
        "@type": "Organization",
        "@id": f"{MAIN_SITE}/#organization",
        "name": "AfraViva",
        "alternateName": "AfricaNext Opportunities (ANO)",
        "url": f"{MAIN_SITE}/",
        "logo": f"{MAIN_SITE}{static('img/afraviva-logo.png')}",
    }
    social = [link.url for link in context.get("MEDIA_SOCIAL_LINKS") or []]
    if social:
        org["sameAs"] = social
    offices = list(context.get("OFFICE_LOCATIONS") or [])
    if offices:
        org["address"] = {"@type": "PostalAddress", "streetAddress": " ".join(offices[0].address.split())}
    return org


def _script(data):
    # "<" escaped so text like "</script>" in a post can't end the tag early.
    payload = json.dumps({"@context": "https://schema.org", **data}, ensure_ascii=False).replace("<", "\u003c")
    return mark_safe(f'<script type="application/ld+json">{payload}</script>')


@register.simple_tag(takes_context=True)
def organization_jsonld(context):
    return _script(_organization(context))


@register.simple_tag(takes_context=True)
def article_jsonld(context, obj, section):
    """`section` is "AfraViva Media" or "AfraViva Farms"."""
    origin = context.get("SITE_ORIGIN", MAIN_SITE)
    request = context.get("request")
    data = {
        "@type": "Article",
        "headline": obj.title[:110],
        "description": Truncator(strip_tags(obj.body)).words(30),
        "articleSection": section,
        "url": request.build_absolute_uri() if request else origin,
        "author": {"@id": f"{MAIN_SITE}/#organization", "@type": "Organization", "name": "AfraViva"},
        "publisher": _organization(context),
    }
    if obj.cover_image:
        data["image"] = f"{origin}{obj.cover_image.url}"
    if obj.published_at:
        data["datePublished"] = obj.published_at.isoformat()
    if obj.updated_at:
        data["dateModified"] = obj.updated_at.isoformat()
    return _script(data)
