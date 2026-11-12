from ai_engine.rag.ingestion import ingest_document
from ai_engine.rag.retriever import retrieve_documents

def ingest_project_document(file_path: str, project_id: str) -> int:
    return ingest_document(file_path, project_id)

def retrieve_project_context(query: str, project_id: str, k: int = 4):
    documents = retrieve_documents(query, project_id, k)
    return documents
