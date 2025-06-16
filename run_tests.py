import unittest
import sys
import os

def main():
    print("Running tests...")  # Debug print
    project_root = os.path.dirname(os.path.abspath(__file__))
    tests_dir = os.path.join(project_root, "src", "tests")

    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    src_dir = os.path.join(project_root, "src")
    if src_dir not in sys.path:
        sys.path.insert(0, src_dir)

    os.chdir(project_root)

    print(f"Discovering tests in: {tests_dir}")  # Debug print
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=tests_dir)
    print(f"Found {suite.countTestCases()} test cases.")  # Debug print
    if suite.countTestCases() == 0:
        print("No tests found. Check your test file names and locations.")
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    sys.exit(not result.wasSuccessful())

if __name__ == "__main__":
    main()