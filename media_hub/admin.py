from django.contrib import admin

from .models import MediaPost


@admin.register(MediaPost)
class MediaPostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "is_published", "published_at")
    list_filter = ("is_published",)
    search_fields = ("title", "body")
    prepopulated_fields = {"slug": ("title",)}

    def save_model(self, request, obj, form, change):
        if not obj.author_id:
            obj.author = request.user
        super().save_model(request, obj, form, change)
