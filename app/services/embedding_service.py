import time
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from app.core.config import GOOGLE_API_KEY


class EmbeddingService:
    def __init__(self):
        self.model = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001",
            google_api_key=GOOGLE_API_KEY
        )

    def embed_text(self, chunks, batch_size=20):
        all_embeddings = []

        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i + batch_size]

            embeddings = self._embed_with_retry(batch)
            all_embeddings.extend(embeddings)

            time.sleep(1)

        return all_embeddings

    def embed_query(self, query):
        return self._embed_with_retry([query])[0]

    def _embed_with_retry(self, batch):
        for attempt in range(5):
            try:
                return self.model.embed_documents(batch)

            except Exception as e:
                if "429" in str(e):
                    time.sleep(10)
                else:
                    raise e

        raise Exception("Embedding failed after retries")