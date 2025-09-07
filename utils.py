# utils.py
import pdfplumber
from io import BytesIO

def extract_text_from_pdf(file_bytes_or_obj):
    """
    Accepts bytes or a file-like object and returns extracted text.
    """
    if isinstance(file_bytes_or_obj, (bytes, bytearray)):
        f = BytesIO(file_bytes_or_obj)
    else:
        f = file_bytes_or_obj

    text = ""
    with pdfplumber.open(f) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()
