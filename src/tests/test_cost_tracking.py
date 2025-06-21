import unittest
from src.scripts.peft_hyperparam_sweep import estimate_local_cost

class TestCostTracking(unittest.TestCase):
    def test_cpu_only_cost(self):
        cost = estimate_local_cost(runtime_seconds=3600, cpu_percent=50, mode="prod")
        self.assertGreater(cost, 0)

    def test_gpu_cost(self):
        cost = estimate_local_cost(runtime_seconds=3600, cpu_percent=50, gpu_load=0.5, mode="prod")
        self.assertGreater(cost, 0)

    def test_dev_mode_cost(self):
        cost = estimate_local_cost(runtime_seconds=3600, cpu_percent=50, mode="dev")
        self.assertEqual(cost, 0)  # Dev mode assumes no cost

if __name__ == "__main__":
    unittest.main()