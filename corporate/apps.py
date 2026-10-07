from django.apps import AppConfig


class CorporateConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'corporate'

    def ready(self):
        _stream_ranged_static_files_through_django()


def _stream_ranged_static_files_through_django():
    """Range requests for static files (every browser's first request for a
    <video>) came back as a bare 500 from the host's LiteSpeed server.

    For a Range request WhiteNoise hands Django a SlicedFile, and Django passes
    any file-backed response to the server's wsgi.file_wrapper. LiteSpeed's
    wrapper can't send a slice of a file, so it fails before Django ever sees
    an error. Clearing file_to_stream for sliced files makes Django iterate the
    slice itself; whole-file responses still use the fast path.
    """
    from whitenoise.middleware import WhiteNoiseFileResponse
    from whitenoise.responders import SlicedFile

    if getattr(WhiteNoiseFileResponse, "_afraviva_range_patch", False):
        return

    original = WhiteNoiseFileResponse._set_streaming_content

    def _set_streaming_content(self, value):
        original(self, value)
        if isinstance(value, SlicedFile):
            self.file_to_stream = None

    WhiteNoiseFileResponse._set_streaming_content = _set_streaming_content
    WhiteNoiseFileResponse._afraviva_range_patch = True
