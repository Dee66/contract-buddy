import sys
import os
import unittest
import logging
from src.adapters.environment import setup_logging, get_mode

# --- Universal Path Fix ---
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)  # noqa: E402


def run_all_tests():
    """
    Discovers and runs all tests in the 'src/tests' directory.
    """
    setup_logging()
    logging.info(f"Running tests in '{get_mode()}' environment.")
    logging.info("Starting test suite execution...")

    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover(start_dir="src/tests", pattern="test_*.py")
    logging.info(f"Found {test_suite.countTestCases()} test cases to execute.")

    test_runner = unittest.TextTestRunner()
    result = test_runner.run(test_suite)

    if not result.wasSuccessful():
        logging.error("Test suite failed. See details above.")
        sys.exit(1)
    else:
        logging.info("Test suite passed successfully.")


if __name__ == "__main__":
    run_all_tests()
