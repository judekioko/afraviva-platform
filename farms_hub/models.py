from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from corporate.validators import validate_image_upload


class FarmUpdate(models.Model):
    CATEGORY_CHOICES = [
        ("crop", "Crop"),
        ("livestock", "Livestock"),
        ("infrastructure", "Infrastructure"),
        ("community", "Community"),
    ]

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    body = models.TextField()
    cover_image = models.ImageField(upload_to="farm_updates/", blank=True, null=True, validators=[validate_image_upload])
    location = models.CharField(max_length=120, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="crop")
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
        return reverse("farms_hub:detail", kwargs={"slug": self.slug})
