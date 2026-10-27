import io
import shutil
import tempfile

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from PIL import Image

from farms_hub.models import FarmCategory, FarmPhoto, FarmUpdate


def _jpeg_with_gps():
    exif = Image.Exif()
    exif[0x0110] = "Test Phone"  # camera model
    exif.get_ifd(0x8825)[2] = (1.0, 17.0, 0.0)  # GPS latitude
    buf = io.BytesIO()
    Image.new("RGB", (40, 30), "green").save(buf, format="JPEG", exif=exif)
    return SimpleUploadedFile("farm.jpg", buf.getvalue(), content_type="image/jpeg")


class ImageMetadataTests(TestCase):
    def setUp(self):
        self.media = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.media, ignore_errors=True)

    def test_uploaded_photo_is_saved_without_exif_or_gps(self):
        with override_settings(MEDIA_ROOT=self.media):
            update = FarmUpdate.objects.create(title="Harvest", body="b", category=FarmCategory.objects.first())
            photo = FarmPhoto.objects.create(update=update, image=_jpeg_with_gps())
            with Image.open(photo.image.path) as img:
                self.assertEqual(len(img.getexif()), 0)
                self.assertEqual(img.size, (40, 30))
