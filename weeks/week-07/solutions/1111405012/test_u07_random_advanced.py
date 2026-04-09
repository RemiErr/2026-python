from __future__ import annotations

import unittest

from test_support import load_topic_versions


MODULES = load_topic_versions("u07-random-advanced")


class TestU07RandomAdvanced(unittest.TestCase):
    def test_repeatable_sequence(self) -> None:
        for version, module in MODULES.items():
            with self.subTest(version=version):
                self.assertEqual(
                    module.repeatable_random_sequence(42),
                    module.repeatable_random_sequence(42),
                )
                self.assertNotEqual(
                    module.repeatable_random_sequence(42),
                    module.repeatable_random_sequence(43),
                )

    def test_independent_random_values(self) -> None:
        for version, module in MODULES.items():
            with self.subTest(version=version):
                value_a, value_b = module.independent_random_values(1, 2)
                self.assertNotEqual(value_a, value_b)
                self.assertGreaterEqual(value_a, 0.0)
                self.assertLess(value_a, 1.0)
                self.assertGreaterEqual(value_b, 0.0)
                self.assertLess(value_b, 1.0)

    def test_secure_helpers(self) -> None:
        for version, module in MODULES.items():
            with self.subTest(version=version):
                number = module.secure_number(100)
                token_hex = module.secure_hex_token(16)
                token_bytes = module.secure_bytes_token(16)
                self.assertGreaterEqual(number, 0)
                self.assertLess(number, 100)
                self.assertEqual(len(token_hex), 32)
                self.assertEqual(len(token_bytes), 16)
                int(token_hex, 16)


if __name__ == "__main__":
    unittest.main()
