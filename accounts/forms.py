from django import forms
from django.contrib.auth import get_user_model

from .models import SignupRequest


class SignupRequestForm(forms.ModelForm):
    # Honeypot: real visitors never see or fill this field (hidden off-screen by
    # CSS, not type="hidden", since some bots skip literal hidden inputs but still
    # autofill everything else). Any value here means it wasn't a human. Same
    # pattern as enquiries.forms.EnquiryForm.
    hp_website = forms.CharField(required=False, widget=forms.TextInput(attrs={
        "autocomplete": "off", "tabindex": "-1",
    }))

    class Meta:
        model = SignupRequest
        fields = ["full_name", "email"]

    def clean_hp_website(self):
        value = self.cleaned_data.get("hp_website")
        if value:
            raise forms.ValidationError("Submission rejected.")
        return value

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if get_user_model().objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        if SignupRequest.objects.filter(email__iexact=email, status=SignupRequest.STATUS_PENDING).exists():
            raise forms.ValidationError("A request for this email is already pending approval.")
        return email
