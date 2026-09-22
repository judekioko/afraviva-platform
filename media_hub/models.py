from django.conf import settings
from django.db import models
from django.utils.text import slugify

from corporate.validators import validate_image_upload, validate_video_upload


def youtube_or_vimeo_embed_url(url):
    """Turn a YouTube/Vimeo watch link into an embeddable iframe URL, using
    the privacy-enhanced YouTube domain. Falls through to the raw URL for
    anything already embed-shaped or from another provider.
    """
    if not url:
        return ""
    if "youtu.be/" in url:
        video_id = url.split("youtu.be/")[-1].split("?")[0]
        return f"https://www.youtube-nocookie.com/embed/{video_id}"
    if "watch?v=" in url:
        video_id = url.split("watch?v=")[-1].split("&")[0]
        return f"https://www.youtube-nocookie.com/embed/{video_id}"
    if "vimeo.com/" in url:
        video_id = url.rstrip("/").split("/")[-1]
        return f"https://player.vimeo.com/video/{video_id}"
    return url


class MediaPost(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    body = models.TextField()
    cover_image = models.ImageField(upload_to="media_posts/", blank=True, null=True, validators=[validate_image_upload])
    video_url = models.URLField(
        blank=True,
        help_text="A YouTube or Vimeo link to embed. Leave blank if uploading a video file below instead.",
    )
    video_file = models.FileField(
        upload_to="media_videos/", blank=True, null=True, validators=[validate_video_upload],
        help_text="Upload a video file directly (under 200MB). Leave blank if using a YouTube/Vimeo link instead.",
    )
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    published_at = models.DateTimeField(blank=True, null=True)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-published_at", "-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        # Always the real subdomain, not a local reverse() — this model's
        # detail page only exists there, and this URL gets rendered both
        # from media.afraviva.com's own pages and from afraviva.com's
        # homepage teasers, where media_hub isn't in the urlconf at all.
        return f"https://media.afraviva.com/{self.slug}/"

    @property
    def video_embed_url(self):
        return youtube_or_vimeo_embed_url(self.video_url)


class MediaVideo(models.Model):
    """An extra video embed on a MediaPost, beyond its one lead video_url/
    video_file — for posts that need several YouTube/Vimeo links (e.g. a
    testimonial plus supporting clips). Rendered below the article body,
    in `order`.
    """

    post = models.ForeignKey(MediaPost, on_delete=models.CASCADE, related_name="videos")
    url = models.URLField(help_text="A YouTube or Vimeo link to embed.")
    caption = models.CharField(max_length=255, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.caption or self.url

    @property
    def embed_url(self):
        return youtube_or_vimeo_embed_url(self.url)
