from __future__ import annotations

import importlib.util
from pathlib import Path
import subprocess
import sys
import unittest


BASE_DIR = Path(__file__).resolve().parent
SOURCE_FILES = [
    "question-10170.py",
    "question-10170-easy.py",
    "question-10170-su.py",
]


def load_module(filename: str):
    path = BASE_DIR / filename
    module_name = filename.replace("-", "_").replace(".", "_")
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def brute_force(start_people: int, day_number: int) -> int:
    people = start_people
    remaining_days = day_number
    while remaining_days > people:
        remaining_days -= people
        people += 1
    return people


class Question10170Tests(unittest.TestCase):
    """確認旅館題的數學解法和模擬結果一致。"""

    @classmethod
    def setUpClass(cls) -> None:
        cls.modules = {name: load_module(name) for name in SOURCE_FILES}

    def test_small_values(self) -> None:
        for start_people in range(1, 11):
            for day_number in range(1, 101):
                raw_input = f"{start_people} {day_number}\n"
                expected = str(brute_force(start_people, day_number))
                for filename, module in self.modules.items():
                    with self.subTest(
                        start_people=start_people,
                        day_number=day_number,
                        filename=filename,
                    ):
                        self.assertEqual(module.solve(raw_input), expected)

    def test_multiple_lines(self) -> None:
        raw_input = "1 3\n3 10\n10 1\n"
        expected = "\n".join(
            str(brute_force(s, d))
            for s, d in [(1, 3), (3, 10), (10, 1)]
        )
        for filename, module in self.modules.items():
            with self.subTest(filename=filename):
                self.assertEqual(module.solve(raw_input), expected)

    def test_command_line_smoke(self) -> None:
        raw_input = "4 4\n4 5\n"
        expected = "\n".join(str(brute_force(s, d)) for s, d in [(4, 4), (4, 5)])
        result = subprocess.run(
            [sys.executable, str(BASE_DIR / "question-10170-su.py")],
            input=raw_input,
            text=True,
            capture_output=True,
            check=True,
        )
        self.assertEqual(result.stdout.strip(), expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
