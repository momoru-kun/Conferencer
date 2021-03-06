from rest_framework import renderers

class FileRenderer(renderers.BaseRenderer):
    media_type = 'application/octet-stream'
    format = 'xlsx'
    def render(self, data, media_type=None, renderer_context=None):
        return data