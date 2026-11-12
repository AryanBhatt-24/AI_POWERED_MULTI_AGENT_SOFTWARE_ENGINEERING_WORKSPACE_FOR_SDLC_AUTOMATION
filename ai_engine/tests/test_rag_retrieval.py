from ai_engine.rag.embeddings import embeddings
from ai_engine.rag.vector_store import vector_store


query = "Can users assign tasks to team members?"

# Step 1: Generate query embedding
print("1. Generating query embedding...", flush=True)

query_embedding = embeddings.embed_query(query)

print("PASS: Query embedding generated.", flush=True)


# Step 2: Direct ChromaDB retrieval
print("2. Searching ChromaDB...", flush=True)

results = vector_store._collection.query(
    query_embeddings=[query_embedding],
    n_results=4,
    where={"project_id": "project_101"},
    include=["documents", "metadatas", "distances"]
)

# Step 3: Verify results
documents = results["documents"][0]

if documents:
    print("\nPASS: Document retrieval successful!")
    for i, document in enumerate(documents):
        print(f"\nDocument {i + 1}:")
        print(document)
        print("Metadata:", results["metadatas"][0][i])
else:
    print("\nFAIL: No matching documents found.")