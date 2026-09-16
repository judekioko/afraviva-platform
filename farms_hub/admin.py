from django.contrib import admin

from .models import FarmUpdate


@admin.register(FarmUpdate)
class FarmUpdateAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "location", "author", "is_published", "published_at")
    list_filter = ("is_published", "category")
    search_fields = ("title", "body", "location")
    prepopulated_fields = {"slug": ("title",)}

    def save_model(self, request, obj, form, change):
        if not obj.author_id:
            obj.author = request.user
        super().save_model(request, obj, form, change)
