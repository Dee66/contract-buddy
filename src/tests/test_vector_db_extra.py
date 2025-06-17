import unittest
from src.storage.vectordb import VectorDB

class TestVectorDBExtra(unittest.TestCase):
    def setUp(self):
        self.db = VectorDB()

    def test_duplicate_ids(self):
        self.db.add("id1", [0.1, 0.2, 0.3])
        self.db.add("id1", [0.4, 0.5, 0.6])  # Should overwrite or update
        results = self.db.query([0.4, 0.5, 0.6], top_k=1)
        self.assertTrue(results)
        self.assertEqual(results[0]['id'], "id1")

    def test_empty_query(self):
        results = self.db.query([0.0, 0.0, 0.0], top_k=1)
        self.assertEqual(results, [])

    def test_missing_vector(self):
        # Query before any add
        db2 = VectorDB()
        results = db2.query([1.0, 2.0, 3.0], top_k=1)
        self.assertEqual(results, [])

    def test_add_and_query_empty(self):
        db = VectorDB()
        db.add("id_empty", [])
        results = db.query([], top_k=1)
        self.assertEqual(results, [])

if __name__ == "__main__":
    unittest.main()