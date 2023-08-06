import os.path

from reportlab.lib.styles import StyleSheet1, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import TableStyle

project_path = os.path.dirname(os.path.abspath(__file__))

pdfmetrics.registerFont(TTFont('Roboto', os.path.join(project_path, 'font', 'Roboto-Thin.ttf')))
pdfmetrics.registerFont(TTFont('Roboto-Italic', os.path.join(project_path, 'font', 'Roboto-ThinItalic.ttf')))
pdfmetrics.registerFont(TTFont('Roboto-Bold', os.path.join(project_path, 'font', 'Roboto-Regular.ttf')))


def getStyleSheet():
    """Returns a stylesheet object"""
    stylesheet = StyleSheet1()

    stylesheet.add(ParagraphStyle(
        name='default',
        fontName='Roboto',
        fontSize=10,
        leading=10,
        leftIndent=0,
        rightIndent=0,
        firstLineIndent=0,
        alignment=TA_LEFT,
        spaceBefore=0,
        spaceAfter=0,
        textColor=colors.black,
        backColor=None,
        wordWrap=None,
        borderWidth=0,
        borderPadding=0,
        borderColor=None,
        borderRadius=None,
        allowWidows=1,
        allowOrphans=0,
        textTransform=None,  # 'uppercase' | 'lowercase' | None
        endDots=None,
        splitLongWords=1))

    stylesheet.add(ParagraphStyle(
        name='bold',
        parent=stylesheet['default'],
        fontName='Roboto-Bold'))

    stylesheet.add(ParagraphStyle(
        name='italic',
        parent=stylesheet['default'],
        fontName='Roboto-Italic'))

    stylesheet.add(ParagraphStyle(
        name='default_list',
        parent=stylesheet['default'],
        leading=15))

    stylesheet.add(ParagraphStyle(
        name='default_number_list',
        parent=stylesheet['default'],
        alignment=TA_RIGHT,
        rightIndent=20,
        leftIndent=10))

    stylesheet.add(ParagraphStyle(
        name='title',
        parent=stylesheet['default'],
        alignment=TA_CENTER,
        fontSize=14,
        leading=20,
        spaceBefore=0,
        spaceAfter=0))

    stylesheet.add(ParagraphStyle(
        name='default_center',
        parent=stylesheet['default'],
        alignment=TA_CENTER))

    stylesheet.add(ParagraphStyle(
        name='header',
        parent=stylesheet['default'],
        alignment=TA_LEFT,
        fontSize=11,
        leading=20,
        spaceBefore=0,
        spaceAfter=0))

    stylesheet.add(ParagraphStyle(
        name='sub_table_header',
        parent=stylesheet['default'],
        leftIndent=7))

    stylesheet.add(ParagraphStyle(
        name='table_header',
        parent=stylesheet['default'],
        fontName='Roboto-Bold'))

    stylesheet.add(ParagraphStyle(
        name='header_center',
        parent=stylesheet['default'],
        fontName='Roboto-Bold',
        alignment=TA_CENTER))

    stylesheet.add(ParagraphStyle(
        name='default_bullet',
        parent=stylesheet['default'],
        bulletColor=colors.black,
        value='square',
        bulletFontSize=1,
        bulletIndent=2))

    return stylesheet


def getTableStyles():
    tablestyles = {'left': TableStyle([
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT')
    ]), 'left_box': TableStyle([
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black)
    ]), 'symptoms': TableStyle([
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT')
    ]), 'top_align': TableStyle([
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('VALIGN', (0, 0), (-1, -1), 'TOP')
    ]), 'treatment_table': TableStyle([
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('SPAN', (0, 0), (1, 0)),
        ('BOX', (0, 0), (-1, -1), 1, colors.black)
    ]), 'exam_table': TableStyle([
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (0, -1), 'TOP'),
        ('LINEBELOW', (0, 0), (-1, -2), 0.25, colors.black),
    ])}

    return tablestyles
