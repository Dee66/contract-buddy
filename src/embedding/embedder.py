from typing import List
import numpy as np

class CodeEmbedder:
    """
    Converts code/text chunks into vector embeddings using a production model.
    Includes error handling and batching for robustness and scalability.
    """
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2", batch_size: int = 32, logger=None):
        self.model_name = model_name
        self.batch_size = batch_size
        self.logger = logger
        self.model = self._load_model()

    def _load_model(self):
        try:
            from sentence_transformers import SentenceTransformer
            return SentenceTransformer(self.model_name)
        except ImportError:
            raise ImportError(
                "Please install sentence-transformers: pip install sentence-transformers"
            )

    def embed_chunks(self, chunks: List[str]) -> List[np.ndarray]:
        """
        Converts a list of text/code chunks into embeddings, with batching and error handling.
        """
        embeddings = []
        for i in range(0, len(chunks), self.batch_size):
            batch = chunks[i:i+self.batch_size]
            try:
                batch_embeddings = self.model.encode(batch, convert_to_numpy=True)
                embeddings.extend(batch_embeddings)
            except Exception as e:
                if self.logger:
                    self.logger.error(f"Embedding failed for batch {i}-{i+len(batch)}: {e}")
                else:
                    print(f"Embedding failed for batch {i}-{i+len(batch)}: {e}")
                # Optionally, append None or skip failed batch
                embeddings.extend([None] * len(batch))
        return embeddings