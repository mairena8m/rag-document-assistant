from pathlib import Path
from pypdf import PdfReader


def load_txt(file_path: str) -> str:
    return Path(file_path).read_text(encoding="utf-8", errors="ignore")


def load_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)
    pages_text = []

    for page in reader.pages:
        text = page.extract_text()
        if text:
            pages_text.append(text)

    return "\n".join(pages_text)


def load_document(file_path: str) -> str:
    suffix = Path(file_path).suffix.lower()

    if suffix == ".txt":
        return load_txt(file_path)

    if suffix == ".pdf":
        return load_pdf(file_path)

    raise ValueError("Formato no soportado. Usa PDF o TXT.")