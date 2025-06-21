import unittest
import os
from src.scripts.run_showcase_pipeline import main

class TestPipelineStress(unittest.TestCase):
    def test_large_dataset(self):
        # Generate a large dataset for testing
        large_data_path = "data/clean/large_docs.json"
        os.makedirs(os.path.dirname(large_data_path), exist_ok=True)
        with open(large_data_path, "w", encoding="utf-8") as f:
            f.write('[{"content": "docstring"}]' * 10000)  # Simulate 10,000 entries
        try:
            main()  # Run the pipeline
        except Exception as e:
            self.fail(f"Pipeline failed under stress: {e}")
        finally:
            os.remove(large_data_path)

if __name__ == "__main__":
    unittest.main()