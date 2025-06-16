import unittest
from chunking.chunker import CodeChunker

class TestCodeChunker(unittest.TestCase):
    def test_basic_chunking(self):
        chunker = CodeChunker(max_chunk_size=10)
        text = "abcdefghij1234567890"
        chunks = chunker.chunk(text)
        self.assertTrue(all(len(chunk) <= 10 for chunk in chunks))
        self.assertEqual("".join(chunks), text)

    def test_empty_input(self):
        chunker = CodeChunker(max_chunk_size=10)
        self.assertEqual(chunker.chunk(""), [])

if __name__ == "__main__":
    unittest.main()