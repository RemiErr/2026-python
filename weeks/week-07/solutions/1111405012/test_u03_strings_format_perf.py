from __future__ import annotations

import unittest

from test_support import load_topic_versions


MODULES = load_topic_versions("u03-strings-format-perf")


class TestU03StringsFormatPerf(unittest.TestCase):
    def test_concat_methods(self) -> None:
        parts = ["item0", "item1", "item2"]
        expected = "item0item1item2"

        for version, module in MODULES.items():
            with self.subTest(version=version):
                self.assertEqual(module.concat_with_plus(parts), expected)
                self.assertEqual(module.concat_with_join(parts), expected)

    def test_safe_format(self) -> None:
        template = "{name} has {n} messages."
        mapping = {"name": "Guido"}

        for version, module in MODULES.items():
            with self.subTest(version=version):
                self.assertEqual(module.safe_format(template, mapping), "Guido has {n} messages.")

    def test_text_and_bytes_behavior(self) -> None:
        for version, module in MODULES.items():
            with self.subTest(version=version):
                self.assertEqual(module.first_text_character("Hello"), "H")
                self.assertEqual(module.first_byte_value(b"Hello"), 72)
                self.assertEqual(module.format_to_ascii_bytes("ACME", 100), b"ACME         100")


if __name__ == "__main__":
    unittest.main()
