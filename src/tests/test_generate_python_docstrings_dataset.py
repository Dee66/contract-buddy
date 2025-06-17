import unittest
import os
from src.scripts import generate_python_docstrings_dataset

class TestGeneratePythonDocstringsDataset(unittest.TestCase):
    def setUp(self):
        self.output_path = "data/clean/docs.json"
        if os.path.exists(self.output_path):
            os.remove(self.output_path)

    def test_docstring_extraction(self):
        docs, failed = generate_python_docstrings_dataset.extract_docstrings(["os"], max_per_module=2)
        self.assertTrue(isinstance(docs, list))
        self.assertTrue(all("content" in d for d in docs))

    def test_deduplicate_docs_removes_duplicates(self):
        docs = [{"content": "foo"}, {"content": "foo"}, {"content": "bar"}]
        unique = generate_python_docstrings_dataset.deduplicate_docs(docs)
        self.assertEqual(len(unique), 2)
        self.assertTrue(any(d["content"] == "foo" for d in unique))
        self.assertTrue(any(d["content"] == "bar" for d in unique))

    def tearDown(self):
        if os.path.exists(self.output_path):
            os.remove(self.output_path)

if __name__ == "__main__":
    unittest.main()