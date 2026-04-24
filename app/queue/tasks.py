from app.queue.celery_app import celery_app
from app.services.vector_store import add_documents
from app.utils.text_utils import chunk_text
import re
import logging

logger = logging.getLogger(__name__)

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    text = text.replace('\n', ' ')
    return text.strip()

@celery_app.task
def process_document(doc_id: str, text: str):
    logger.info(f"Processing doc_id={doc_id}")
    text=clean_text(text)
    chunks = chunk_text(text)

    add_documents(doc_id, chunks)

    logger.info(f"Stored {len(chunks)} chunks for doc {doc_id}")

    return {
        "doc_id": doc_id,
        "chunks": len(chunks),
        "status": "processed"
    }
