import unittest
import os
import yaml
from src.utils import environment

class TestEnvironmentConfig(unittest.TestCase):
    def setUp(self):
        # Create a temporary config file
        self.config_path = "temp_test_config.yaml"
        self.yaml_content = """
environment: staging
dev:
  foo: 1
staging:
  foo: 2
prod:
  foo: 3
"""
        with open(self.config_path, "w", encoding="utf-8") as f:
            f.write(self.yaml_content)

    def tearDown(self):
        if os.path.exists(self.config_path):
            os.remove(self.config_path)
        if "CB_ENV" in os.environ:
            del os.environ["CB_ENV"]

    def test_get_mode_from_yaml(self):
        os.environ.pop("CB_ENV", None)
        mode = environment.get_mode()
        self.assertIn(mode, ["dev", "staging", "prod"])

    def test_env_config_switching(self):
        os.environ["CB_ENV"] = "prod"
        env_config = environment.get_env_config(self.config_path)
        self.assertEqual(env_config["foo"], 3)
        os.environ["CB_ENV"] = "dev"
        env_config = environment.get_env_config(self.config_path)
        self.assertEqual(env_config["foo"], 1)
        os.environ["CB_ENV"] = "staging"
        env_config = environment.get_env_config(self.config_path)
        self.assertEqual(env_config["foo"], 2)

if __name__ == "__main__":
    unittest.main()