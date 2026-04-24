from fastapi import FastAPI, UploadFile, File
import uuid
from app.services.document_loader import load_document
from app.queue.tasks import process_document
from app.services.vector_store import search
from app.services.gemini_service import generate_answer
from pypdf import PdfReader
from app.utils.text_utils import chunk_text
from app.services.vector_store import add_documents
from app.services.embedding_service import EmbeddingService
import io

from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

app = FastAPI()
embedding_service = EmbeddingService()

@app.post("/upload")
async def upload(file: UploadFile):
    content = await file.read()
    text = extract_text(file, content)
    chunks = chunk_text(text)
    add_documents("doc1", chunks)  # DIRECT CALL (no celery)
    print("Chunks:", len(chunks))
    # print("Vectors:", len(vectors))
    # print("FAISS size:", self.index.ntotal)
    return {"status": "processed"}

@app.get("/query")
def query_docs(q: str):
    results = search(q, top_k=10)
    if not results:
        return {"answer": "No relevant data found", "context": []}
    query_vector = embedding_service.embed_query(q)
    ranked = rerank(query_vector, results, embedding_service)
    context = "\n\n".join([r["text"] for r in ranked])
    answer = generate_answer(q, context)
    # print("FAISS size:", self.index.ntotal)
    # print("Retrieved:", len(results))
    return {
        "query": q,
        "answer": answer,
        "sources": [
            {
                "doc_id": r["doc_id"],
                "chunk_id": r["chunk_id"]
            } for r in ranked
        ]
    }

def extract_text(file, content):
    if file.filename.endswith(".pdf"):
        reader = PdfReader(io.BytesIO(content))
        return " ".join([page.extract_text() or "" for page in reader.pages])
    else:
        return content.decode("utf-8")
    
def rerank(query_vector, results, embedding_service, top_k=3):
    texts = [r["text"] for r in results]

    doc_vectors = embedding_service.embed_text(texts)

    sims = cosine_similarity(
        [query_vector],
        doc_vectors
    )[0]

    ranked = sorted(
        zip(results, sims),
        key=lambda x: x[1],
        reverse=True
    )

    return [item[0] for item in ranked[:top_k]]
