from pathlib import Path
from langchain_chroma import Chroma
from ai_engine.rag.embeddings import embeddings

ROOT_DIR = Path(__file__).resolve().parents[2]

VECTOR_DB_PATH = ROOT_DIR / "storage" / "vector_db"

vector_store = Chroma(
    collection_name="sdlc_documents",
    embedding_function=embeddings,
    persist_directory=str(VECTOR_DB_PATH)
)