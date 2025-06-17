import unittest
from src.ingestion.sources.github import fetch_github_repos

class DummyLogger:
    def debug(self, *args, **kwargs): pass
    def info(self, *args, **kwargs): pass
    def warning(self, *args, **kwargs): pass
    def error(self, *args, **kwargs): pass

class TestDataIngestion(unittest.TestCase):
    def test_fetch_github_repos(self):
        # Use a public repo for a safe test, or mock requests in a real test suite
        repos = ["octocat/Hello-World"]
        results = fetch_github_repos(repos, logger=DummyLogger())
        self.assertIsInstance(results, list)
        if results:
            self.assertIn("repo", results[0])
            self.assertIn("readme", results[0])

if __name__ == "__main__":
    unittest.main()