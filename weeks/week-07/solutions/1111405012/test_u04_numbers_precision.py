from __future__ import annotations

import unittest
from decimal import Decimal

from test_support import load_topic_versions


MODULES = load_topic_versions("u04-numbers-precision")


class TestU04NumbersPrecision(unittest.TestCase):
    def test_bankers_round(self) -> None:
        for version, module in MODULES.items():
            with self.subTest(version=version):
                self.assertEqual(module.bankers_round(0.5), 0)
                self.assertEqual(module.bankers_round(2.5), 2)
                self.assertEqual(module.bankers_round(3.5), 4)

    def test_traditional_round(self) -> None:
        for version, module in MODULES.items():
            with self.subTest(version=version):
                self.assertEqual(module.traditional_round(0.5), Decimal("1"))
                self.assertEqual(module.traditional_round(2.5), Decimal("3"))
                self.assertEqual(module.traditional_round(2.675, 2), Decimal("2.68"))

    def test_nan_and_decimal_examples(self) -> None:
        values = [1.0, float("nan"), 3.0, float("nan")]

        for version, module in MODULES.items():
            with self.subTest(version=version):
                self.assertTrue(module.is_nan(float("nan")))
                self.assertEqual(module.remove_nan(values), [1.0, 3.0])
                self.assertEqual(module.decimal_sum(), Decimal("0.3"))
                self.assertFalse(module.float_equals_point_three())
                self.assertTrue(module.decimal_equals_point_three())


if __name__ == "__main__":
    unittest.main()
