import unittest
from src.scripts.peft_hyperparam_sweep import main

class TestPeftSweepEdgeCases(unittest.TestCase):
    def test_invalid_hyperparameters(self):
        # Simulate invalid hyperparameters
        invalid_params = {"lora_rs": [-1], "lora_alphas": [0]}
        with self.assertRaises(ValueError):
            main(config=invalid_params)

    def test_empty_dataset(self):
        # Simulate an empty dataset
        empty_data_path = "data/clean/empty_pairs.json"
        with open(empty_data_path, "w", encoding="utf-8") as f:
            f.write("[]")
        with self.assertRaises(Exception):
            main(dataset_path=empty_data_path)

if __name__ == "__main__":
    unittest.main()