from django.conf import settings
from django.db import models
from django.utils.text import slugify

from corporate.validators import validate_image_upload


class FarmCategory(models.Model):
    name = models.CharField(max_length=60)
    slug = models.SlugField(max_length=60, unique=True, blank=True)
    order = models.PositiveIntegerField(default=0)
    published = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name_plural = "Farm categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class FarmUpdate(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    body = models.TextField()
    cover_image = models.ImageField(upload_to="farm_updates/", blank=True, null=True, validators=[validate_image_upload])
    location = models.CharField(max_length=120, blank=True)
    category = models.ForeignKey(
        FarmCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name="updates",
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
        # from farms.afraviva.com's own pages and from afraviva.com's
        # homepage teasers, where farms_hub isn't in the urlconf at all.
        return f"https://farms.afraviva.com/{self.slug}/"
