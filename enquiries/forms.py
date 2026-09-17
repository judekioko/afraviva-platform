from django import forms

from .models import Enquiry


class EnquiryForm(forms.ModelForm):
    # Honeypot: real visitors never see or fill this field (hidden off-screen by
    # CSS, not type="hidden", since some bots skip literal hidden inputs but still
    # autofill everything else). Any value here means it wasn't a human.
    hp_website = forms.CharField(required=False, widget=forms.TextInput(attrs={
        "autocomplete": "off", "tabindex": "-1",
    }))

    class Meta:
        model = Enquiry
        fields = ["name", "email", "phone", "message"]
        widgets = {
            "message": forms.Textarea(attrs={"rows": 5}),
        }

    def clean_hp_website(self):
        value = self.cleaned_data.get("hp_website")
        if value:
            raise forms.ValidationError("Submission rejected.")
        return value
