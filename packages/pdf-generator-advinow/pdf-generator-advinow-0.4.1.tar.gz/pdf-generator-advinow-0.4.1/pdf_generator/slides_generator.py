from io import BytesIO

from PIL import Image as PILImage
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import StyleSheet1, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Image, Paragraph, Spacer

from .utils import stretch_image_size


class PDFSlidesGenerator:
    """
    This class is used for generation of PDF from measurements images
    """
    def __init__(self):
        self._buffer = BytesIO()
        self.doc = SimpleDocTemplate(self._buffer, pagesize=letter)
        self.frame_width = self.doc.width - 12  # 12 is default indent here
        self.frame_height = self.doc.height - 12
        self.elements = []
        self.styles = StyleSheet1()
        self.set_styles()

    def set_styles(self):
        self.styles.add(
            ParagraphStyle(name='normal', fontSize=18))
        self.styles.add(
            ParagraphStyle(name='title', fontSize=20, alignment=TA_CENTER))

    def add_spacer(self, height=12):
        self.elements.append(Spacer(self.frame_width, height))

    @staticmethod
    def _generate_image(stream, prefered_width, max_height):
        image = PILImage.open(stream)
        stream.seek(0)
        image_stretch = stretch_image_size(image.width, image.height, prefered_width, max_height)
        return Image(stream, image_stretch['width'], image_stretch['height'])

    def add_image(self, image):
        flowable_image = self._generate_image(image, self.frame_width, self.frame_height)
        self.elements.append(flowable_image)
        self.add_spacer()

    def add_caption(self, caption, style='normal'):
        caption_style = self.styles.get(style)
        flowable_caption = Paragraph(text=caption, style=caption_style)
        self.elements.append(flowable_caption)
        self.add_spacer()

    def render(self):
        self.doc.build(self.elements)
        self._buffer.seek(0)
        return self._buffer
