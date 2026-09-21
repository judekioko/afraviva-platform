from django.shortcuts import render

from enquiries.forms import EnquiryForm
from farms_hub.models import FarmUpdate
from media_hub.models import MediaPost

from .models import (
    AboutCard,
    FAQItem,
    HeroSlide,
    InsightPublication,
    OfficeLocation,
    PartnerCard,
    ServiceCard,
    TeamMember,
    VisionPillar,
)


def home(request):
    context = {
        "media_teasers": MediaPost.objects.filter(is_published=True)[:3],
        "farm_teasers": FarmUpdate.objects.filter(is_published=True).select_related("category")[:3],
        "hero_slides": list(HeroSlide.objects.filter(published=True).values("headline", "subhead")),
        "services": ServiceCard.objects.filter(published=True),
        "partners": PartnerCard.objects.filter(published=True),
        "vision_pillars": VisionPillar.objects.filter(published=True),
        "insights": InsightPublication.objects.filter(published=True)[:3],
    }
    return render(request, "corporate/home.html", context)


def about(request):
    context = {
        "team": TeamMember.objects.filter(published=True),
        "mission_cards": AboutCard.objects.filter(published=True, section=AboutCard.SECTION_MISSION),
        "different_cards": AboutCard.objects.filter(published=True, section=AboutCard.SECTION_DIFFERENT),
    }
    return render(request, "corporate/about.html", context)


def services(request):
    context = {
        "services": ServiceCard.objects.filter(published=True),
        "partners": PartnerCard.objects.filter(published=True),
    }
    return render(request, "corporate/services.html", context)


def thrivepoint(request):
    context = {"insights": InsightPublication.objects.filter(published=True)}
    return render(request, "corporate/thrivepoint.html", context)


def faq(request):
    context = {"faqs": FAQItem.objects.filter(published=True)}
    return render(request, "corporate/faq.html", context)


def contact(request):
    context = {"form": EnquiryForm(), "offices": OfficeLocation.objects.filter(published=True)}
    return render(request, "corporate/contact.html", context)
