import unittest
import sys
import os

if __name__ == "__main__":
    # Ensure the project root is in sys.path for absolute imports
    sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
    # Discover and run all tests in the 'tests' directory
    unittest.TextTestRunner(verbosity=2).run(
        unittest.defaultTestLoader.discover('tests')
    )