from __future__ import annotations

import importlib.util
from itertools import combinations
from pathlib import Path
import subprocess
import sys
import unittest


BASE_DIR = Path(__file__).resolve().parent
SOURCE_FILES = [
    "question-10071.py",
    "question-10071-easy.py",
    "question-10071-su.py",
]


def load_module(filename: str):
    path = BASE_DIR / filename
    module_name = filename.replace("-", "_").replace(".", "_")
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def brute_force(numbers: list[int]) -> int:
    total = 0
    for a in numbers:
        for b in numbers:
            for c in numbers:
                for d in numbers:
                    for e in numbers:
                        for f in numbers:
                            if a + b + c + d + e == f:
                                total += 1
    return total


class Question10071Tests(unittest.TestCase):
    """驗證五數和等於第六個數的計數結果。"""

    @classmethod
    def setUpClass(cls) -> None:
        cls.modules = {name: load_module(name) for name in SOURCE_FILES}

    def test_all_small_sets(self) -> None:
        candidates = [-2, -1, 0, 1, 2]
        for size in range(1, 5):
            for picked in combinations(candidates, size):
                numbers = list(picked)
                raw_input = "\n".join([str(len(numbers))] + [str(x) for x in numbers]) + "\n"
                expected = str(brute_force(numbers))
                for filename, module in self.modules.items():
                    with self.subTest(numbers=numbers, filename=filename):
                        self.assertEqual(module.solve(raw_input), expected)

    def test_command_line_smoke(self) -> None:
        raw_input = "3\n-1\n0\n2\n"
        expected = str(brute_force([-1, 0, 2]))
        result = subprocess.run(
            [sys.executable, str(BASE_DIR / "question-10071-su.py")],
            input=raw_input,
            text=True,
            capture_output=True,
            check=True,
        )
        self.assertEqual(result.stdout.strip(), expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
