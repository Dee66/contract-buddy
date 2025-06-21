import faiss
import numpy as np
import json
import os
from typing import List, Dict, Any
from src.domain.ports import IVectorRepository
from src.domain.entities import Chunk


class FaissVectorRepository(IVectorRepository):
    """
    A concrete implementation of the IVectorRepository port using FAISS.
    This adapter manages an in-memory (and optionally persisted) FAISS index
    for efficient similarity searches. It is ideal for local development.
    """

    def __init__(
        self, embedding_dim: int, persist_path: str = "outputs/storage/faiss_index.bin"
    ):
        self.embedding_dim = embedding_dim
        self.persist_path = persist_path
        self.index_path = self.persist_path
        self.id_map_path = self.persist_path.replace(".bin", "_ids.json")

        dir_name = os.path.dirname(self.persist_path)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)

        if os.path.exists(self.index_path):
            self.index = faiss.read_index(self.index_path)
            with open(self.id_map_path, "r") as f:
                self.id_map = json.load(f)
        else:
            self.index = faiss.IndexFlatL2(self.embedding_dim)
            self.id_map = []

    def add(self, chunks: List[Chunk]):
        """Adds chunks and their embeddings to the index."""
        embeddings = np.array(
            [chunk.embedding for chunk in chunks if chunk.embedding is not None]
        ).astype("float32")
        if embeddings.shape[0] > 0:
            self.index.add(embeddings)
            self.id_map.extend(
                [chunk.id for chunk in chunks if chunk.embedding is not None]
            )

    def search(
        self,
        query_embedding: np.ndarray,
        top_k: int,
        metadata_filter: Dict[str, Any] = None,
    ) -> List[Chunk]:
        """
        Performs a similarity search on the index.
        Note: This basic implementation does not support metadata filtering.
        A production system would require a more advanced index or a hybrid search approach.
        """
        if self.index.ntotal == 0:
            return []
        query_embedding_np = np.array([query_embedding]).astype("float32")
        distances, indices = self.index.search(query_embedding_np, top_k)

        # This basic implementation doesn't use metadata_filter, but a real one would.
        # For now, we return placeholder chunks. A full implementation would retrieve
        # the chunk content from a separate store using the IDs.
        results = []
        for i in indices[0]:
            if i != -1:
                chunk_id = self.id_map[i]
                results.append(
                    Chunk(
                        id=chunk_id,
                        document_id="retrieved_doc",
                        content=f"Content for {chunk_id}",
                    )
                )
        return results

    def persist(self):
        """Saves the index and metadata to disk."""
        faiss.write_index(self.index, self.index_path)
        with open(self.id_map_path, "w") as f:
            json.dump(self.id_map, f)

    @classmethod
    def load(cls, persist_path: str, embedding_dim: int = 0):
        # This method is for convenience, __init__ handles loading logic.
        repo = cls(embedding_dim=embedding_dim, persist_path=persist_path)
        if repo.index and repo.index.d > 0:
            repo.embedding_dim = repo.index.d
        return repo
