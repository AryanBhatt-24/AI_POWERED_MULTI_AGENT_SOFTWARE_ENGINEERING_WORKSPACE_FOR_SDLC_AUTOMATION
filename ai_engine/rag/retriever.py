from ai_engine.rag.vector_store import vector_store

def retrieve_documents(query: str, project_id: str, k: int = 4):
    results = vector_store.similarity_search(
        query=query,
        k=k,
        filter={'project_id':project_id}
    )

    return results
    