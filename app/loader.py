import os
from typing import List
from PyPDF2 import PdfReader

def load_text_file(path: str) -> str:
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def load_pdf_file(path: str) -> str:
    reader = PdfReader(path)
    return "\n".join([page.extract_text() or "" for page in reader.pages])

def load_documents(directory: str) -> List[dict]:
    supported_exts = {'.md', '.txt', '.py', '.pdf'}
    docs = []
    
    for filename in os.listdir(directory):
        path = os.path.join(directory, filename)
        _, ext = os.path.splitext(filename)

        if ext.lower() not in supported_exts:
            continue

        try:
            if ext == '.pdf':
                text = load_pdf_file(path)
            else:
                text = load_text_file(path)
            docs.append({"filename": filename, "text": text})
        except Exception as e:
            print(f"[ERROR] Failed to load {filename}: {e}")

    return docs
