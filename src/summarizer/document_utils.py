from PyPDF2 import PdfReader
import docx


def extract_text_from_txt(txt_file):
    # For TXT files
    text = txt_file.read().decode("utf-8")
    return text


def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text


def extract_text_from_docx(docx_file):
    doc = docx.Document(docx_file)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text
