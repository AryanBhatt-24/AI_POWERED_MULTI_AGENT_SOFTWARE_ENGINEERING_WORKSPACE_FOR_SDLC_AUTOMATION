from pathlib import Path
from pypdf import PdfReader
from docx import Document as DocxDocument
from langchain_core.documents import Document

def load_pdf(file_path: str) -> list[Document]:
    documents = []

    reader = PdfReader(file_path)

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text()

        if text and text.strip():
            documents.append(
                Document(
                    page_content=text,
                    metadata={
                        "source": str(file_path),
                        "file_type": "pdf",
                        "page": page_number
                    }
                )
            )
    
    return documents

def load_docx(file_path: str) -> list[Document]:
    doc = DocxDocument(file_path)

    text = "\n".join(
        paragraph.text
        for paragraph in doc.paragraphs
        if paragraph.text.strip()
    )

    if not text.strip():
        return []
    
    return [
        Document(
            page_content=text,
            metadata={
                "source": str(file_path),
                "file_type": "docx"
            }
        )
    ]

def load_text(file_path: str) -> list[Document]:
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()

    if not text.strip():
        return []
    
    return [
        Document(
            page_content=text,
            metadata={
                "source": str(file_path), 
                "file_type": "text"
            }
        )
    ]

def load_document(file_path: str) -> list[Document]:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    extension = path.suffix.lower()

    if extension == '.pdf':
        return load_pdf(file_path)
    
    elif extension == '.docx':
        return load_docx(file_path)
    
    elif extension == '.txt':
        return load_text(file_path)
    
    else:
        raise ValueError(f"Unsupported file format: {extension}")
