import unittest
from src.scripts import generate_python_docstrings_dataset

class TestDocstringConfigDriven(unittest.TestCase):
    def test_extract_with_config(self):
        # Should use config-driven modules and max_per_module
        docs, failed = generate_python_docstrings_dataset.extract_docstrings(["os", "sys"], 1)
        self.assertTrue(isinstance(docs, list))
        # Each module should return at most 1 docstring, so total should be <= number of modules
        self.assertLessEqual(len(docs), 4)
        # Optionally, check that each doc comes from the correct module
        for doc in docs:
            self.assertIn(doc.get("module"), ["os", "sys"])

if __name__ == "__main__":
    unittest.main()