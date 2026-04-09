from __future__ import annotations

import unittest

from test_support import load_topic_versions


MODULES = load_topic_versions("r_01_iterator_basics")


class TestR01IteratorBasics(unittest.TestCase):
    def test_consume_helpers(self) -> None:
        for version, module in MODULES.items():
            with self.subTest(version=version):
                self.assertEqual(module.consume_with_next([1, 2, 3]), [1, 2, 3])
                self.assertEqual(module.consume_with_default(["a", None, "c"]), ["a", None, "c"])

    def test_countdown_iterator(self) -> None:
        for version, module in MODULES.items():
            with self.subTest(version=version):
                self.assertEqual(list(module.CountDown(3)), [3, 2, 1])
                iterator = iter(module.CountDown(2))
                self.assertEqual(next(iterator), 2)
                self.assertEqual(next(iterator), 1)
                with self.assertRaises(StopIteration):
                    next(iterator)

    def test_iterable_and_iterator_checks(self) -> None:
        for version, module in MODULES.items():
            with self.subTest(version=version):
                plain_list = [1, 2, 3]
                real_iterator = iter(plain_list)
                self.assertTrue(module.is_iterable(plain_list))
                self.assertFalse(module.is_iterator(plain_list))
                self.assertTrue(module.is_iterable(real_iterator))
                self.assertTrue(module.is_iterator(real_iterator))
                self.assertFalse(module.is_iterable(10))


if __name__ == "__main__":
    unittest.main()
