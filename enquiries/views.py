from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render
from django.template.loader import render_to_string
from django_ratelimit.decorators import ratelimit

from .forms import EnquiryForm


@ratelimit(key="ip", rate="5/h", method="POST", block=True)
def submit_enquiry(request):
    """HTMX endpoint: validates + saves an Enquiry, emails staff, returns a partial."""
    if request.method == "POST":
        form = EnquiryForm(request.POST)
        if form.is_valid():
            enquiry = form.save()
            if settings.ENQUIRY_NOTIFY_TO:
                send_mail(
                    subject=f"New enquiry from {enquiry.name} ({enquiry.source_page or 'website'})",
                    message=render_to_string("enquiries/email_notification.txt", {"enquiry": enquiry}),
                    from_email=settings.EMAIL_HOST_USER or "noreply@afraviva.com",
                    recipient_list=settings.ENQUIRY_NOTIFY_TO,
                    fail_silently=True,
                )
            return render(request, "enquiries/_success.html", {"enquiry": enquiry})
        return render(request, "enquiries/_form.html", {"form": form}, status=400)

    return render(request, "enquiries/_form.html", {"form": EnquiryForm()})
