from django.contrib import admin

from .models import FAQItem, TeamMember

admin.site.site_header = "AfricaNext Opportunities Admin"
admin.site.site_title = "AfricaNext Opportunities Admin"
admin.site.index_title = "Content management — AfraViva Media, Farms, Homes and corporate"


@admin.register(FAQItem)
class FAQItemAdmin(admin.ModelAdmin):
    list_display = ("question", "order", "published")
    list_editable = ("order", "published")


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ("name", "role", "order", "published")
    list_editable = ("order", "published")
