from typing import List, Dict, Any
import numpy as np

class VectorDB:
    """
    Simple FAISS-based vector DB for local development and testing.
    """
    def __init__(self, dim: int = 384):
        # Store vectors as a dict: id -> vector (numpy array)
        self.vectors: Dict[str, np.ndarray] = {}

    def upsert(self, ids: List[str], vectors: List[List[float]]):
        """
        Add or update vectors in the database.
        """
        for id_, vec in zip(ids, vectors):
            self.vectors[id_] = np.array(vec, dtype=float)

    def add(self, id_: str, vector: List[float]):
        """
        Add or update a single vector.
        """
        self.vectors[id_] = np.array(vector, dtype=float)

    def query(self, vector: List[float], top_k: int = 1) -> List[Dict[str, Any]]:
        """
        Return the top_k most similar vectors to the input vector.
        """
        if not self.vectors:
            return []
        query_vec = np.array(vector, dtype=float)
        similarities = []
        for id_, vec in self.vectors.items():
            # Cosine similarity
            sim = np.dot(query_vec, vec) / (np.linalg.norm(query_vec) * np.linalg.norm(vec) + 1e-8)
            similarities.append((id_, sim))
        similarities.sort(key=lambda x: x[1], reverse=True)
        return [{"id": id_, "score": score} for id_, score in similarities[:top_k]]