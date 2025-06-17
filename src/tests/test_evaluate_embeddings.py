import unittest
import os
import json
from src.embedding import evaluate_embeddings

class TestEvaluateEmbeddings(unittest.TestCase):
    def setUp(self):
        # Create dummy pairs
        self.pairs_path = "data/clean/contrastive_pairs.json"
        os.makedirs(os.path.dirname(self.pairs_path), exist_ok=True)
        pairs = [["A", "B"], ["C", "D"]]
        with open(self.pairs_path, "w", encoding="utf-8") as f:
            json.dump(pairs, f)

    def test_negative_pairs(self):
        pairs = [["A", "B"], ["C", "D"], ["E", "F"]]
        negatives = evaluate_embeddings.generate_negative_pairs(pairs)
        self.assertTrue(len(negatives) > 0)
        self.assertTrue(all(len(pair) == 2 for pair in negatives))

    def test_generate_negative_pairs_empty(self):
        pairs = []
        negatives = evaluate_embeddings.generate_negative_pairs(pairs)
        self.assertEqual(negatives, [])

    def tearDown(self):
        if os.path.exists(self.pairs_path):
            os.remove(self.pairs_path)

if __name__ == "__main__":
    unittest.main()