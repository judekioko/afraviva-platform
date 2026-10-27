"""Strips EXIF and other metadata (GPS location, camera serial, capture time)
from every image uploaded through the admin, before it is saved.

Phone photos often carry the exact place they were taken; publishing that for
farm workers, families or children would disclose personal data the Privacy
Policy doesn't mention. Orientation is applied to the pixels first, so photos
still display the right way up.
"""

import io

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import ImageField
from django.db.models.signals import pre_save
from PIL import Image, ImageOps

FORMATS = {"JPEG", "PNG", "WEBP"}


def _clean(field_file):
    field_file.open()
    field_file.seek(0)
    with Image.open(field_file) as img:
        fmt = img.format
        if fmt not in FORMATS:
            return None
        img = ImageOps.exif_transpose(img)
        out = io.BytesIO()
        options = {"quality": 90, "optimize": True} if fmt in {"JPEG", "WEBP"} else {"optimize": True}
        if fmt == "JPEG" and img.mode not in ("RGB", "L"):
            img = img.convert("RGB")
        img.save(out, format=fmt, **options)  # no exif= / pnginfo= → metadata is dropped
    out.seek(0)
    return InMemoryUploadedFile(out, None, field_file.name, Image.MIME[fmt], out.getbuffer().nbytes, None)


def strip_uploaded_image_metadata(sender, instance, **kwargs):
    for field in sender._meta.get_fields():
        if not isinstance(field, ImageField):
            continue
        field_file = getattr(instance, field.attname)
        if not field_file or getattr(field_file, "_committed", True):
            continue  # nothing new uploaded on this save
        cleaned = _clean(field_file)
        if cleaned is not None:
            field_file.file = cleaned


def connect():
    pre_save.connect(strip_uploaded_image_metadata, dispatch_uid="strip_uploaded_image_metadata")
