from django import forms

from .models import Enquiry


class EnquiryForm(forms.ModelForm):
    class Meta:
        model = Enquiry
        fields = ["name", "email", "phone", "source_page", "message"]
        widgets = {
            "source_page": forms.HiddenInput(),
            "message": forms.Textarea(attrs={"rows": 5}),
        }
