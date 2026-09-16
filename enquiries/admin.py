from django.contrib import admin

from .models import Enquiry


@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "source_page", "status", "created_at")
    list_filter = ("status", "source_page")
    list_editable = ("status",)
    search_fields = ("name", "email", "message")
    readonly_fields = ("name", "email", "phone", "source_page", "message", "created_at")
