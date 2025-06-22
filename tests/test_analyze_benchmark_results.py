import sys
import os
import unittest
from unittest.mock import patch
import json
import tempfile
import shutil

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from scripts.analyze_benchmark_results import main as analyze_main  # noqa: E402


class TestAnalyzeBenchmarkResults(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.input_dir = os.path.join(self.test_dir, "input")
        self.output_dir = os.path.join(self.test_dir, "output")
        os.makedirs(self.input_dir)
        os.makedirs(self.output_dir)

        results1 = {
            "model_name": "model_a",
            "top_1_accuracy": 0.95,
            "avg_inference_time_ms": 100,
        }
        with open(os.path.join(self.input_dir, "eval_results_1.json"), "w") as f:
            json.dump(results1, f)

        results2 = {
            "model_name": "model_b",
            "top_1_accuracy": 0.92,
            "avg_inference_time_ms": 120,
        }
        with open(os.path.join(self.input_dir, "eval_results_2.json"), "w") as f:
            json.dump(results2, f)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_script_runs_and_creates_output(self):
        with patch("sys.argv", ["script_name", self.input_dir, self.output_dir]):
            analyze_main()

        self.assertTrue(
            os.path.exists(os.path.join(self.output_dir, "benchmark_report.csv"))
        )
        self.assertTrue(
            os.path.exists(os.path.join(self.output_dir, "benchmark_report.md"))
        )
        self.assertTrue(os.path.exists(os.path.join(self.output_dir, "best_run.json")))

        with open(os.path.join(self.output_dir, "best_run.json"), "r") as f:
            best_run = json.load(f)
        self.assertEqual(best_run["model_name"], "model_a")
        self.assertAlmostEqual(best_run["top_1_accuracy"], 0.95)


if __name__ == "__main__":
    unittest.main()
