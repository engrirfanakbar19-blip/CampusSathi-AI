from pathlib import Path
from pypdf import PdfReader

DOCUMENTS_FOLDER = Path("data/documents")


def read_pdf(pdf_path):
    text = ""

    reader = PdfReader(pdf_path)

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


def load_documents():

    documents = []

    # TXT files
    for file_path in DOCUMENTS_FOLDER.glob("*.txt"):

        text = file_path.read_text(
            encoding="utf-8"
        )

        documents.append({
            "source": file_path.name,
            "text": text
        })

    # PDF files
    for file_path in DOCUMENTS_FOLDER.glob("*.pdf"):

        text = read_pdf(file_path)

        documents.append({
            "source": file_path.name,
            "text": text
        })

    return documents