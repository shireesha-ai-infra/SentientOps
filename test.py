from src.ingest import load_pdfs

texts = load_pdfs("data/pdf_files")
print(type(texts))