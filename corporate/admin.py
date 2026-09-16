from django.contrib import admin

from .models import FAQItem, TeamMember


@admin.register(FAQItem)
class FAQItemAdmin(admin.ModelAdmin):
    list_display = ("question", "order", "published")
    list_editable = ("order", "published")


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ("name", "role", "order", "published")
    list_editable = ("order", "published")
