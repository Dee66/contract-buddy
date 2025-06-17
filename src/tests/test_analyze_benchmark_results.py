import unittest
import os
import json
from src.scripts import analyze_benchmark_results

class TestAnalyzeBenchmarkResults(unittest.TestCase):
    def setUp(self):
        self.results_path = "data/clean/hyperparam_sweep_results.json"
        os.makedirs(os.path.dirname(self.results_path), exist_ok=True)
        results = [
            {
                "hyperparams": {"r": 4, "alpha": 16, "dropout": 0.0},
                "peft_retrieval": {"top1": 0.5, "mrr": 0.7},
                "timing_seconds": 1.0,
                "memory_usage_mb": 100.0
            }
        ]
        with open(self.results_path, "w", encoding="utf-8") as f:
            json.dump(results, f)

    def test_script_runs(self):
        # Just check that the script runs without error
        analyze_benchmark_results.main()

    def tearDown(self):
        if os.path.exists(self.results_path):
            os.remove(self.results_path)

if __name__ == "__main__":
    unittest.main()