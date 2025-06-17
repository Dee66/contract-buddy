import unittest
from src.embedding.embedder import CodeEmbedder

class TestCodeEmbedder(unittest.TestCase):
    def test_embedding_shape(self):
        embedder = CodeEmbedder(model_name="sentence-transformers/all-MiniLM-L6-v2")
        vecs = embedder.embed_chunks(["test string"])
        self.assertIsInstance(vecs, list)
        self.assertEqual(len(vecs), 1)
        import numpy as np
        self.assertIsInstance(vecs[0], np.ndarray)

if __name__ == "__main__":
    unittest.main()