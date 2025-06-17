import unittest
from src.embedding.embedder import CodeEmbedder

class TestCodeEmbedderExtra(unittest.TestCase):
    def setUp(self):
        self.embedder = CodeEmbedder(model_name="sentence-transformers/all-MiniLM-L6-v2")

    def test_batch_embedding(self):
        texts = ["foo", "bar", "baz"]
        vecs = self.embedder.embed_chunks(texts)
        self.assertEqual(len(vecs), 3)

    def test_empty_list(self):
        vecs = self.embedder.embed_chunks([])
        self.assertEqual(vecs, [])

    def test_embedder_non_string_input(self):
        with self.assertRaises(Exception):
            self.embedder.embed_chunks([None, 123, {}])

if __name__ == "__main__":
    unittest.main()