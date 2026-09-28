from io import BytesIO

from docx import Document
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer


def format_txt(content: str) -> bytes:
    return content.encode("utf-8")


def format_docx(content: str, document_type: str, terms: list[str]) -> bytes:
    document = Document()
    document.add_heading(document_type, level=0)
    for paragraph in content.splitlines():
        if paragraph.strip():
            document.add_paragraph(paragraph.strip())

    output = BytesIO()
    document.save(output)
    return output.getvalue()


def format_pdf(content: str, document_type: str, terms: list[str]) -> bytes:
    output = BytesIO()
    document = SimpleDocTemplate(output, pagesize=LETTER)
    styles = getSampleStyleSheet()
    story = [Paragraph(document_type, styles["Title"]), Spacer(1, 12)]
    for paragraph in content.splitlines():
        if paragraph.strip():
            story.append(Paragraph(paragraph.strip(), styles["BodyText"]))
            story.append(Spacer(1, 6))
    document.build(story)
    return output.getvalue()