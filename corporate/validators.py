"""Shared upload validators. All image uploads in this project are admin-only
(no public-facing upload form exists), so the threat model is a compromised or
careless staff account, not an anonymous attacker — these are deliberately
generous caps to catch mistakes and resource-exhaustion, not a tight filter.
"""

from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions

MAX_UPLOAD_SIZE_MB = 10
MAX_DIMENSION_PX = 6000
MAX_DOCUMENT_SIZE_MB = 15
MAX_VIDEO_SIZE_MB = 200


def validate_image_upload(file):
    if file.size > MAX_UPLOAD_SIZE_MB * 1024 * 1024:
        raise ValidationError(f"Image must be under {MAX_UPLOAD_SIZE_MB}MB.")

    width, height = get_image_dimensions(file)
    if width and height and (width > MAX_DIMENSION_PX or height > MAX_DIMENSION_PX):
        raise ValidationError(f"Image dimensions must be under {MAX_DIMENSION_PX}x{MAX_DIMENSION_PX}px.")


def validate_document_upload(file):
    if file.size > MAX_DOCUMENT_SIZE_MB * 1024 * 1024:
        raise ValidationError(f"File must be under {MAX_DOCUMENT_SIZE_MB}MB.")


def validate_video_upload(file):
    if file.size > MAX_VIDEO_SIZE_MB * 1024 * 1024:
        raise ValidationError(f"Video must be under {MAX_VIDEO_SIZE_MB}MB.")
