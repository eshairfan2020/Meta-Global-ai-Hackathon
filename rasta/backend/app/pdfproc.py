import pdfplumber
from fastapi import UploadFile

MAX_PDF_CHARS = 20000  # matches AnalyzeRequest.text limit

async def extract_pdf_text(file: UploadFile) -> str:
    with pdfplumber.open(file.file) as pdf:
        text = "\n".join(page.extract_text() or "" for page in pdf.pages)
    return text[:MAX_PDF_CHARS]