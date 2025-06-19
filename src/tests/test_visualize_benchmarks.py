import unittest
import os
import json
from src.scripts import visualize_benchmarks

class TestVisualizeBenchmarks(unittest.TestCase):
    def setUp(self):
        self.results_path = "data/clean/hyperparam_sweep_results.json"
        os.makedirs(os.path.dirname(self.results_path), exist_ok=True)
        results = [
            {
                "hyperparams": {"r": 4, "alpha": 16, "dropout": 0.0},
                "peft_retrieval": {"top1": 0.5, "mrr": 0.7},
                "timing_seconds": 1.0,
                "estimated_cost_usd": 0.01
            }
        ]
        with open(self.results_path, "w", encoding="utf-8") as f:
            json.dump(results, f)

    def test_visualization_runs(self):
        # Should create PNG files without error
        visualize_benchmarks.main()
        self.assertTrue(os.path.exists("data/clean/benchmark_top1_vs_cost.png"))

    def tearDown(self):
        for fname in [
            "data/clean/hyperparam_sweep_results.json",
            "data/clean/benchmark_top1_vs_cost.png",
            "data/clean/benchmark_runtime_vs_cost.png",
            "data/clean/benchmark_top1_vs_runtime_cost.png",
        ]:
            if os.path.exists(fname):
                os.remove(fname)

if __name__ == "__main__":
    unittest.main()