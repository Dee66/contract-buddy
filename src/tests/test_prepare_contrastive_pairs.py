import unittest
import os
import json
from src.embedding import prepare_contrastive_pairs

class TestPrepareContrastivePairs(unittest.TestCase):
    def setUp(self):
        # Create a small docs.json for testing
        self.docs_path = "data/clean/docs.json"
        self.pairs_path = "data/clean/contrastive_pairs.json"
        os.makedirs(os.path.dirname(self.docs_path), exist_ok=True)
        docs = [{"content": f"Chunk {i}"} for i in range(5)]
        with open(self.docs_path, "w", encoding="utf-8") as f:
            json.dump(docs, f)

    def test_pairs_created(self):
        prepare_contrastive_pairs.main()
        self.assertTrue(os.path.exists(self.pairs_path))
        with open(self.pairs_path, "r", encoding="utf-8") as f:
            pairs = json.load(f)
        self.assertTrue(len(pairs) > 0)
        self.assertTrue(all(len(pair) == 2 for pair in pairs))

    def tearDown(self):
        if os.path.exists(self.pairs_path):
            os.remove(self.pairs_path)
        if os.path.exists(self.docs_path):
            os.remove(self.docs_path)

if __name__ == "__main__":
    unittest.main()