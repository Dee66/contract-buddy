import unittest
import sys
import os
import yaml
from src.utils.environment import setup_logging

def load_and_set_env(config_path="config.yaml"):
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    env = config.get("environment", "dev")
    os.environ["MODE"] = env  # For legacy code
    os.environ["CB_ENV"] = env  # For new code

def main():
    setup_logging()
    load_and_set_env()  # Ensure environment is set for all tests
    logging = __import__("logging")
    logging.info("Running tests...")

    project_root = os.path.dirname(os.path.abspath(__file__))
    tests_dir = os.path.join(project_root, "src", "tests")

    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    src_dir = os.path.join(project_root, "src")
    if src_dir not in sys.path:
        sys.path.insert(0, src_dir)

    os.chdir(project_root)

    logging.info(f"Discovering tests in: {tests_dir}")
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=tests_dir)
    num_tests = suite.countTestCases()
    logging.info(f"Found {num_tests} test cases.")
    if num_tests == 0:
        logging.error("No tests found. Check test file names and locations.")
        sys.exit(1)

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    if not result.wasSuccessful():
        logging.error("Some tests failed.")
        sys.exit(1)
    else:
        logging.info("All tests passed successfully.")

if __name__ == "__main__":
    main()