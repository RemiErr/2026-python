from __future__ import annotations

import unittest

from test_support import load_topic_versions


# 一次載入三個版本，確保教學版與簡化版結果一致。
MODULES = load_topic_versions("u01-strings-split-gotchas")


class TestU01StringsSplitGotchas(unittest.TestCase):
    def test_split_and_rebuild(self) -> None:
        sample = "asdf fjdk; afed, fjek,asdf, foo"
        expected_values = ["asdf", "fjdk", "afed", "fjek", "asdf", "foo"]
        expected_delimiters = [" ", ";", ",", ",", ","]
        expected_rebuilt = "asdf fjdk;afed,fjek,asdf,foo"

        for version, module in MODULES.items():
            with self.subTest(version=version):
                values, delimiters = module.split_preserving_delimiters(sample)
                self.assertEqual(values, expected_values)
                self.assertEqual(delimiters, expected_delimiters)
                self.assertEqual(module.rebuild_text(values, delimiters), expected_rebuilt)

    def test_safe_startswith(self) -> None:
        for version, module in MODULES.items():
            with self.subTest(version=version):
                self.assertTrue(module.safe_startswith("http://www.python.org", ["http:", "ftp:"]))
                self.assertFalse(module.safe_startswith("mailto:test@example.com", ["http:", "ftp:"]))

    def test_normalize_spaces_and_clean_lines(self) -> None:
        lines = ["  apple  \n", "  banana  \n"]

        for version, module in MODULES.items():
            with self.subTest(version=version):
                self.assertEqual(module.normalize_spaces("  hello     world  "), "hello world")
                self.assertEqual(module.clean_lines(lines), ["apple", "banana"])


if __name__ == "__main__":
    unittest.main()
