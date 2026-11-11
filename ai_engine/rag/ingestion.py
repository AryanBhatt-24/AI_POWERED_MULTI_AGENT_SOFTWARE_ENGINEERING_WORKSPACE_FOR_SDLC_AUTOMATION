from ai_engine.rag.loaders import load_document
from ai_engine.rag.chunking import split_documents
from ai_engine.rag.vector_store import vector_store

def ingest_document(file_path: str, project_id: str) -> int:
    documents = load_document(file_path)
    chunks = split_documents(documents)

    if not chunks:
        return 0
    
    for chunk in chunks:
        chunk.metadata["project_id"] = project_id

    ids = vector_store.add_documents(chunks)
    return len(ids)
