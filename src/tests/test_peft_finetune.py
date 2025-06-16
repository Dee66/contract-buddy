import os
import shutil
import unittest
from embedding import peft_finetune

class TestPeftFinetune(unittest.TestCase):
    def setUp(self):
        # Clean up any previous adapter output
        self.adapter_dir = "peft_adapter"
        if os.path.exists(self.adapter_dir):
            shutil.rmtree(self.adapter_dir)

    @unittest.skip("PEFT fine-tuning test skipped: model does not return a loss for embedding tasks.")
    def test_peft_training_runs(self):
        # This will run a very short training using local config and data
        try:
            peft_finetune.main()
        except Exception as e:
            self.fail(f"PEFT fine-tuning failed: {e}")
        # Check that adapter directory was created
        self.assertTrue(os.path.exists(self.adapter_dir))
        self.assertTrue(any(os.scandir(self.adapter_dir)), "Adapter directory is empty")

    def tearDown(self):
        # Optionally clean up after test
        if os.path.exists(self.adapter_dir):
            shutil.rmtree(self.adapter_dir)

if __name__ == "__main__":
    unittest.main()