from __future__ import annotations

import unittest

from test_support import load_topic_versions


MODULES = load_topic_versions("u02-regex-advanced")


class TestU02RegexAdvanced(unittest.TestCase):
    def test_find_dates(self) -> None:
        text = "Today is 11/27/2012. PyCon starts 3/13/2013."
        expected = [("11", "27", "2012"), ("3", "13", "2013")]

        for version, module in MODULES.items():
            with self.subTest(version=version):
                self.assertEqual(module.find_dates_with_module(text), expected)
                self.assertEqual(module.find_dates_with_pattern(text), expected)

    def test_rewrite_dates(self) -> None:
        text = "Today is 11/27/2012. PyCon starts 3/13/2013."
        expected = "Today is 27 Nov 2012. PyCon starts 13 Mar 2013."

        for version, module in MODULES.items():
            with self.subTest(version=version):
                self.assertEqual(module.rewrite_dates(text), expected)

    def test_replace_python_word(self) -> None:
        sample = "UPPER PYTHON, lower python, Mixed Python"
        expected = "UPPER SNAKE, lower snake, Mixed Snake"

        for version, module in MODULES.items():
            with self.subTest(version=version):
                self.assertEqual(module.replace_python_word(sample), expected)


if __name__ == "__main__":
    unittest.main()
