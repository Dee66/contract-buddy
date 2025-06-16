import faiss
import numpy as np
from typing import List

class VectorDB:
    """
    Simple FAISS-based vector DB for local development and testing.
    """
    def __init__(self, dim: int = 384):
        self.index = faiss.IndexFlatL2(dim)
        self.chunks = []

    def upsert(self, chunks: List[str], embeddings: List[np.ndarray]):
        vectors = np.vstack([e for e in embeddings if e is not None]).astype('float32')
        self.index.add(vectors)
        self.chunks.extend(chunks)

    def search(self, query_embedding: np.ndarray, top_k: int = 5):
        D, I = self.index.search(query_embedding.reshape(1, -1).astype('float32'), top_k)
        return [self.chunks[i] for i in I[0] if i < len(self.chunks)]