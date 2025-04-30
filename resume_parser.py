import os
from pdfminer.high_level import extract_text as extract_pdf_text
from docx import Document

def extract_text_from_pdf(file_path):
    try:
        return extract_pdf_text(file_path)
    except Exception as e:
        return f"Error reading PDF: {e}"
    
def extract_text_from_docx(file_path):
    try:
        doc = Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        return f"Error reading DOCX: {e}"
    
def extract_resume_text(file_path):
    _, ext = os.path.splitext(file_path)
    if ext.lower() == '.pdf':
        return extract_text_from_pdf(file_path)
    elif ext.lower() == '.docx':
        return extract_text_from_docx(file_path)
    else:
        return "Unsupported file format. Please upload a PDF or DOCX."

