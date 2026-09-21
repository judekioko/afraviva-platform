from django.contrib import admin

from .models import MediaPost


@admin.register(MediaPost)
class MediaPostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "is_published", "published_at", "has_video")
    list_filter = ("is_published",)
    search_fields = ("title", "body")
    prepopulated_fields = {"slug": ("title",)}

    @admin.display(boolean=True, description="Video")
    def has_video(self, obj):
        return bool(obj.video_url or obj.video_file)

    def save_model(self, request, obj, form, change):
        if not obj.author_id:
            obj.author = request.user
        super().save_model(request, obj, form, change)
