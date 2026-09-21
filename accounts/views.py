from django.contrib.auth.views import PasswordChangeView, PasswordResetConfirmView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils import timezone
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
