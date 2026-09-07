import os
from pypdf import PdfReader
from docx import Document

SUPPORTED_EXTENSIONS = (".txt", ".pdf", ".docx")


def read_txt(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def read_pdf(path: str) -> str:
    reader = PdfReader(path)
    text_parts = [page.extract_text() or "" for page in reader.pages]
    return "\n".join(text_parts)


def read_docx(path: str) -> str:
    doc = Document(path)
    paragraphs = [p.text for p in doc.paragraphs]
    return "\n".join(paragraphs)


def load_document(path: str) -> str:
    ext = os.path.splitext(path)[1].lower()

    if ext == ".txt":
        return read_txt(path)
    elif ext == ".pdf":
        return read_pdf(path)
    elif ext == ".docx":
        return read_docx(path)
    else:
        raise ValueError(f"Format tidak didukung: {ext}")


def load_documents_from_folder(folder_path: str) -> list[tuple[str, str]]:
    """Return list of (source_name, text) untuk setiap file yang didukung di folder."""
    results = []

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(SUPPORTED_EXTENSIONS):
            full_path = os.path.join(folder_path, filename)
            text = load_document(full_path)
            results.append((filename, text))

    return results