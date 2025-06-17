import unittest
from src.cleaning.sensitive_data_filter import SensitiveDataFilter

class TestSensitiveDataFilter(unittest.TestCase):
    def setUp(self):
        # Use a logger that does nothing for test output cleanliness
        class DummyLogger:
            def debug(self, *args, **kwargs): pass
            def info(self, *args, **kwargs): pass
            def exception(self, *args, **kwargs): pass
        self.filter = SensitiveDataFilter(logger=DummyLogger())

    def test_contains_sensitive_data(self):
        self.assertTrue(self.filter.contains_sensitive_data("api_key: ABCDEFGHIJKLMNOP"))
        self.assertFalse(self.filter.contains_sensitive_data("def foo(): pass"))

    def test_filter_sensitive_entries(self):
        entries = [
            "api_key: ABCDEFGHIJKLMNOP",
            "def foo(): pass"
        ]
        filtered = self.filter.filter_sensitive_entries(entries)
        self.assertEqual(filtered, ["def foo(): pass"])

if __name__ == "__main__":
    unittest.main()