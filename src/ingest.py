# Data Ingeston 

from pypdf import PdfReader
from pathlib import Path

def load_pdfs(pdf_dir: str):
    texts = []
    
    for pdf_path in Path(pdf_dir).glob("*.pdf"):
        reader = PdfReader(pdf_path)
        content = ""
        for page in reader.pages:
            content += page.extract_text() or ""
        texts.append(content)

    return texts