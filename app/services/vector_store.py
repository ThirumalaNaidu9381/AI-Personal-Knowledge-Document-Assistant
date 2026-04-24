from app.services.embedding_service import EmbeddingService
from app.services.faiss_store import FAISSStore
import uuid

embedding_service = EmbeddingService()
faiss_store = FAISSStore()

def add_documents(doc_id, chunks):
    vectors = embedding_service.embed_text(chunks)

    metadatas = []
    for i, chunk in enumerate(chunks):
        metadatas.append({
            "doc_id": doc_id,
            "chunk_id": f"{doc_id}_{i}",
            "text": chunk
        })

    faiss_store.add(vectors, metadatas)


def search(query, top_k=5):
    query_vector = embedding_service.embed_query(query)
    results = faiss_store.search(query_vector, top_k)

    return results