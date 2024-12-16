import io
import pdfplumber
import docx


def parse_pdf(file_bytes: bytes) -> str:
    """
    Extract text from a PDF using pdfplumber.
    """
    text = []
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            text.append(page.extract_text())
    return "\n".join(text)


def parse_docx(file_bytes: bytes) -> str:
    # Extract text from Word
    bio = io.BytesIO(file_bytes)
    doc = docx.Document(bio)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return "\n".join(full_text)


def parse_document(file_bytes: bytes, filename: str) -> str:
    if filename.lower().endswith(".pdf"):
        return parse_pdf(file_bytes)
    elif filename.lower().endswith(".docx") or filename.lower().endswith(".doc"):
        return parse_docx(file_bytes)
    else:
        raise ValueError("Unsupported file format. Please upload a PDF or DOCX.")
