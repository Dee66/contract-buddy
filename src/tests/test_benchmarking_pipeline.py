import unittest
import tempfile
import os
import json
from sentence_transformers import SentenceTransformer
import numpy as np

# Import functions from your benchmarking scripts
from embedding.evaluate_embeddings import (
    load_pairs,
    generate_negative_pairs,
    evaluate_model,
    retrieval_metrics
)
from embedding.prepare_contrastive_pairs import (
    load_chunks,
    create_positive_pairs
)

class TestBenchmarkingPipeline(unittest.TestCase):

    def setUp(self):
        # Create dummy data for testing
        self.dummy_chunks = [
            "The quick brown fox jumps over the lazy dog.",
            "A fast brown fox leaps over a sleepy dog.",
            "Python is a programming language.",
            "Java is also a programming language."
        ]
        self.dummy_pairs = [
            [self.dummy_chunks[0], self.dummy_chunks[1]],
            [self.dummy_chunks[2], self.dummy_chunks[3]]
        ]
        # Use a small, fast model for testing
        self.model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    def test_load_chunks(self):
        # Write dummy data to a temp file
        with tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".json") as tf:
            json.dump([{"content": c} for c in self.dummy_chunks], tf)
            tf.flush()
            chunks = load_chunks(tf.name)
        self.assertEqual(len(chunks), len(self.dummy_chunks))
        os.unlink(tf.name)

    def test_create_positive_pairs(self):
        pairs = create_positive_pairs(self.dummy_chunks, num_pairs=2)
        self.assertEqual(len(pairs), 2)
        for a, b in pairs:
            self.assertIn(a, self.dummy_chunks)
            self.assertIn(b, self.dummy_chunks)
            self.assertNotEqual(a, b)

    def test_generate_negative_pairs(self):
        negatives = generate_negative_pairs(self.dummy_pairs)
        self.assertTrue(len(negatives) > 0)
        for a, b in negatives:
            self.assertNotEqual(a, b)

    def test_evaluate_model(self):
        mean_sim, scores = evaluate_model(self.model, self.dummy_pairs)
        self.assertIsInstance(mean_sim, float)
        self.assertEqual(len(scores), len(self.dummy_pairs))

    def test_retrieval_metrics(self):
        negatives = generate_negative_pairs(self.dummy_pairs)
        metrics = retrieval_metrics(self.model, self.dummy_pairs, negatives, top_k=2)
        self.assertIn("top1", metrics)
        self.assertIn("topk", metrics)
        self.assertIn("mrr", metrics)
        self.assertTrue(0 <= metrics["top1"] <= 1)
        self.assertTrue(0 <= metrics["topk"] <= 1)
        self.assertTrue(0 <= metrics["mrr"] <= 1)

    def test_load_pairs(self):
        # Write dummy pairs to a temp file
        with tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".json") as tf:
            json.dump(self.dummy_pairs, tf)
            tf.flush()
            pairs = load_pairs(tf.name, max_pairs=2)
        self.assertEqual(len(pairs), 2)
        os.unlink(tf.name)

if __name__ == "__main__":
    unittest.main()