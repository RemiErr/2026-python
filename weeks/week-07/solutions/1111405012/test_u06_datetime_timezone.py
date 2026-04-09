from __future__ import annotations

import unittest
from datetime import datetime

from test_support import load_topic_versions


MODULES = load_topic_versions("u06-datetime-timezone")


class TestU06DatetimeTimezone(unittest.TestCase):
    def test_dst_boundary(self) -> None:
        for version, module in MODULES.items():
            with self.subTest(version=version):
                central = module.get_timezone("America/Chicago")
                local_dt = datetime(2013, 3, 10, 1, 45, tzinfo=central)
                wrong = module.add_minutes_locally(local_dt, 30)
                correct = module.add_minutes_via_utc(local_dt, 30)
                self.assertEqual(wrong.replace(tzinfo=None).isoformat(), "2013-03-10T02:15:00")
                self.assertEqual(correct.isoformat(), "2013-03-10T03:15:00-05:00")

    def test_parse_and_convert(self) -> None:
        for version, module in MODULES.items():
            with self.subTest(version=version):
                utc_dt = module.parse_local_to_utc("2012-12-21 09:30:00", "America/Chicago")
                taipei_dt = module.convert_utc_to_timezone(utc_dt, "Asia/Taipei")
                self.assertEqual(utc_dt.isoformat(), "2012-12-21T15:30:00+00:00")
                self.assertEqual(taipei_dt.isoformat(), "2012-12-21T23:30:00+08:00")

    def test_requires_aware_datetime(self) -> None:
        naive = datetime(2024, 1, 1, 12, 0, 0)

        for version, module in MODULES.items():
            with self.subTest(version=version):
                with self.assertRaises(ValueError):
                    module.add_minutes_via_utc(naive, 10)
                with self.assertRaises(ValueError):
                    module.convert_utc_to_timezone(naive, "Asia/Taipei")


if __name__ == "__main__":
    unittest.main()
