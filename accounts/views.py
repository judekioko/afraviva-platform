import base64
from io import BytesIO

import qrcode
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView, PasswordResetConfirmView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils import timezone
from django_otp import login as otp_login
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_ratelimit.decorators import ratelimit

from .forms import SignupRequestForm
from .models import StaffProfile


def _stamp_password_changed(user):
    StaffProfile.objects.update_or_create(user=user, defaults={"password_changed_at": timezone.now()})


class StampingPasswordChangeView(PasswordChangeView):
    """Same as Django's own view, plus records when the password changed so
    the expiry middleware knows the clock has been reset.
    """

    success_url = reverse_lazy("accounts:password_change_done")

    def form_valid(self, form):
        response = super().form_valid(form)
        _stamp_password_changed(self.request.user)
        return response


class StampingPasswordResetConfirmView(PasswordResetConfirmView):
    """Same as Django's own view (used both for the initial invite/bootstrap
    link and for a forgotten-password reset), plus records the change.
    """

    success_url = reverse_lazy("accounts:password_reset_complete")

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.user is not None:
            _stamp_password_changed(self.user)
        return response


@ratelimit(key="ip", rate="5/h", method="POST", block=True)
def signup_request(request):
    """Public "request staff access" form. Never creates a login on its own —
    just files a SignupRequest for the super admin to approve from /admin/.
    """
    if request.method == "POST":
        form = SignupRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "accounts/signup_done.html")
    else:
        form = SignupRequestForm()
    return render(request, "accounts/signup.html", {"form": form})


@login_required
def two_factor_setup(request):
    """Self-service TOTP enrollment for staff/admin accounts. Only a confirmed
    device (one whose owner has proven they can generate a valid code) counts —
    an unconfirmed device is just a pending QR code nobody has scanned yet, and
    is recreated each visit rather than piling up abandoned ones.
    """
    existing = TOTPDevice.objects.filter(user=request.user, confirmed=True).first()
    if existing:
        return render(request, "accounts/two_factor_setup.html", {"confirmed": True})

    # Reused across the GET (which shows the QR) and the POST that verifies a
    # code against it — recreating it on every request would invalidate the
    # secret the user just scanned before they get a chance to prove it.
    device = TOTPDevice.objects.filter(user=request.user, confirmed=False).first()
    if device is None:
        device = TOTPDevice.objects.create(user=request.user, confirmed=False, name="default")

    error = None
    if request.method == "POST":
        token = request.POST.get("token", "").strip()
        if device.verify_token(token):
            device.confirmed = True
            device.save()
            otp_login(request, device)
            return render(request, "accounts/two_factor_setup.html", {
                "confirmed": True, "just_confirmed": True,
            })
        error = "That code didn't match — check your phone's clock and try again."

    qr_buffer = BytesIO()
    qrcode.make(device.config_url).save(qr_buffer, format="PNG")
    qr_data_uri = "data:image/png;base64," + base64.b64encode(qr_buffer.getvalue()).decode()
    secret = base64.b32encode(device.bin_key).decode()

    return render(request, "accounts/two_factor_setup.html", {
        "confirmed": False, "qr_data_uri": qr_data_uri, "secret": secret, "error": error,
    })
