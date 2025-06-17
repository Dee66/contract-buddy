import unittest
from src.chunking.chunker import CodeChunker

class TestCodeChunkerExtra(unittest.TestCase):
    def setUp(self):
        self.chunker = CodeChunker(max_chunk_size=5)

    def test_unicode_and_newlines(self):
        text = "αβγδε\nζηθικ\nλμνξο"
        chunks = self.chunker.chunk(text)
        self.assertTrue(all(isinstance(chunk, str) for chunk in chunks))
        self.assertEqual("".join(chunks), text)

    def test_whitespace_only(self):
        text = "     \n   \n"
        chunks = self.chunker.chunk(text)
        self.assertIsInstance(chunks, list)
        self.assertTrue(all(isinstance(chunk, str) for chunk in chunks))

    def test_large_input(self):
        text = "a" * 10000
        chunks = self.chunker.chunk(text)
        self.assertTrue(all(len(chunk) <= 5 for chunk in chunks))
        self.assertEqual("".join(chunks), text)

    def test_chunk_text_with_language(self):
        text = "def foo():\n    pass\n\ndef bar():\n    pass"
        chunks = self.chunker.chunk_text(text, language="python")
        self.assertTrue(isinstance(chunks, list))
        self.assertTrue(all(isinstance(chunk, str) for chunk in chunks))

if __name__ == "__main__":
    unittest.main()