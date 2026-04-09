from __future__ import annotations

import unittest
from datetime import datetime

from test_support import load_topic_versions


MODULES = load_topic_versions("u05-datetime-gotchas")


class TestU05DatetimeGotchas(unittest.TestCase):
    def test_timedelta_month_error(self) -> None:
        for version, module in MODULES.items():
            with self.subTest(version=version):
                self.assertIn("months", module.month_keyword_error().lower())

    def test_add_one_month(self) -> None:
        for version, module in MODULES.items():
            with self.subTest(version=version):
                self.assertEqual(module.add_one_month(datetime(2012, 1, 31)), datetime(2012, 2, 29))
                self.assertEqual(module.add_one_month(datetime(2012, 9, 23)), datetime(2012, 10, 23))

    def test_parse_methods(self) -> None:
        expected = datetime(2012, 9, 20)

        for version, module in MODULES.items():
            with self.subTest(version=version):
                self.assertEqual(module.parse_with_strptime("2012-09-20"), expected)
                self.assertEqual(module.parse_manually("2012-09-20"), expected)


if __name__ == "__main__":
    unittest.main()
