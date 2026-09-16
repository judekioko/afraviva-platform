from django.shortcuts import render

from enquiries.forms import EnquiryForm
from farms_hub.models import FarmUpdate
from media_hub.models import MediaPost

from .models import FAQItem, TeamMember


def home(request):
    context = {
        "media_teasers": MediaPost.objects.filter(is_published=True)[:3],
        "farm_teasers": FarmUpdate.objects.filter(is_published=True)[:3],
    }
    return render(request, "corporate/home.html", context)


def about(request):
    context = {"team": TeamMember.objects.filter(published=True)}
    return render(request, "corporate/about.html", context)


def services(request):
    return render(request, "corporate/services.html")


def thrivepoint(request):
    return render(request, "corporate/thrivepoint.html")


def faq(request):
    context = {"faqs": FAQItem.objects.filter(published=True)}
    return render(request, "corporate/faq.html", context)


def contact(request):
    context = {"form": EnquiryForm(initial={"source_page": "contact"})}
    return render(request, "corporate/contact.html", context)
