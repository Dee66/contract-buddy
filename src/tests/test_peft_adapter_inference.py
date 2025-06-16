import unittest
from embedding.embedder import CodeEmbedder

class TestPeftAdapterInference(unittest.TestCase):
    def test_embedder_with_adapter(self):
        embedder = CodeEmbedder(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            peft_adapter_dir="peft_adapter_contrastive"
        )
        vecs = embedder.embed_chunks(["test string"])
        self.assertIsInstance(vecs, list)
        self.assertTrue(len(vecs) > 0)

if __name__ == "__main__":
    unittest.main()