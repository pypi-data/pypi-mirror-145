import gzip
import unittest
from pathlib import Path

from random_readline import idx, indices_of_newlines, readline

shouldbe = list(
    map(
        lambda x: x + "\n",
        filter(lambda x: x, Path("test/test.txt").read_text().split("\n")),
    )
)


class TestCase(unittest.TestCase):
    def test_idx(self):
        indices = idx(b"abcd\nefg\n")
        self.assertListEqual(indices, [4, 8])

    def test_indices_of_newlines(self):
        with open("test/test.txt", "rb") as fp:
            indices = indices_of_newlines(fp)
        self.assertListEqual(indices, [20, 33, 45, 58, 70, 82, 96, 109, 114])

    def test_readline(self):
        n_lines, read = readline("test/test.txt", shuffle=False)
        lines = [line for line in read()]
        self.assertEqual(n_lines, 9)
        self.assertEqual(len(lines), 9)
        self.assertListEqual(lines, shouldbe)

    def test_readline_shuffle(self):
        n_lines, read = readline("test/test.txt", shuffle=True)
        lines = set([line for line in read()])
        self.assertEqual(n_lines, 9)
        self.assertEqual(len(lines), 9)
        for line in lines:
            self.assertTrue(line in shouldbe)

    def test_readline_chunk_size(self):
        n_lines, read = readline("test/test.txt", shuffle=True, chunk_size=5)
        lines = set([line for line in read()])
        self.assertEqual(n_lines, 9)
        self.assertEqual(len(lines), 9)
        for line in lines:
            self.assertTrue(line in shouldbe)

    def test_readline_opener(self):
        n_lines, read = readline(
            "test/test.txt.gz", shuffle=True, chunk_size=5, opener=gzip.open
        )
        lines = set([line for line in read()])
        self.assertEqual(n_lines, 9)
        self.assertEqual(len(lines), 9)
        for line in lines:
            self.assertTrue(line in shouldbe)


if __name__ == "__main__":
    unittest.main()
