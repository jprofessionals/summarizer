from PyPDF2 import PdfReader
import docx


def extract_text_from_txt(txt_file) -> str:
    """
    Extracts text from a TXT file.

    Args:
        txt_file (file-like object): The text file to extract text from.

    Returns:
        str: The extracted text.
    """
    try:
        text = txt_file.read().decode("utf-8")
    except Exception as e:
        raise ValueError(f"Error reading TXT file: {e}")
    return text


def extract_text_from_pdf(pdf_file) -> str:
    """
    Extracts text from a PDF file.

    Args:
        pdf_file (file-like object): The PDF file to extract text from.

    Returns:
        str: The extracted text.
    """
    try:
        reader = PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    except Exception as e:
        raise ValueError(f"Error reading PDF file: {e}")
    return text


def extract_text_from_docx(docx_file) -> str:
    """
    Extracts text from a DOCX file.

    Args:
        docx_file (file-like object): The DOCX file to extract text from.

    Returns:
        str: The extracted text.
    """
    try:
        doc = docx.Document(docx_file)
        text = ""
        for para in doc.paragraphs:
            text += para.text + "\n"
    except Exception as e:
        raise ValueError(f"Error reading DOCX file: {e}")
    return text
