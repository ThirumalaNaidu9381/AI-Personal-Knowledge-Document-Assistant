import faiss
import numpy as np
import os
import pickle

class FAISSStore:
    def __init__(self, index_path="faiss.index", meta_path="meta.pkl"):
        self.index = None
        self.dimension = None
        self.index_path = index_path
        self.meta_path = meta_path
        self.metadata = []  # stores dict per chunk

        self._load()

    def _init_index(self, vector):
        self.dimension = len(vector)
        self.index = faiss.IndexFlatL2(self.dimension)

    def add(self, vectors, metadatas):
        vectors = np.array(vectors).astype("float32")

        if self.index is None:
            self._init_index(vectors[0])

        self.index.add(vectors)
        self.metadata.extend(metadatas)

        self._save()

    def search(self, query_vector, top_k=5):
        if self.index is None or self.index.ntotal == 0:
            return []

        query_vector = np.array([query_vector]).astype("float32")

        distances, indices = self.index.search(query_vector, top_k)

        results = []
        for idx, dist in zip(indices[0], distances[0]):
            if idx < len(self.metadata):
                item = self.metadata[idx]
                item["score"] = float(dist)
                results.append(item)

        return results

    def _save(self):
        faiss.write_index(self.index, self.index_path)
        with open(self.meta_path, "wb") as f:
            pickle.dump(self.metadata, f)

    def _load(self):
        if os.path.exists(self.index_path):
            self.index = faiss.read_index(self.index_path)

        if os.path.exists(self.meta_path):
            with open(self.meta_path, "rb") as f:
                self.metadata = pickle.load(f)