from __future__ import annotations

import importlib.util
from itertools import permutations
from pathlib import Path
import subprocess
import sys
import unittest


BASE_DIR = Path(__file__).resolve().parent
SOURCE_FILES = [
    "question-10062.py",
    "question-10062-easy.py",
    "question-10062-su.py",
]


def load_module(filename: str):
    path = BASE_DIR / filename
    module_name = filename.replace("-", "_").replace(".", "_")
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def build_case(order: tuple[int, ...]) -> tuple[str, str]:
    smaller_counts = []
    for index, value in enumerate(order[1:], start=1):
        smaller_counts.append(sum(1 for left in order[:index] if left < value))
    input_text = "\n".join([str(len(order))] + [str(x) for x in smaller_counts]) + "\n"
    output_text = "\n".join(str(x) for x in order)
    return input_text, output_text


class Question10062Tests(unittest.TestCase):
    """驗證三個版本都能正確還原牛群順序。"""

    @classmethod
    def setUpClass(cls) -> None:
        cls.modules = {name: load_module(name) for name in SOURCE_FILES}

    def test_all_small_permutations(self) -> None:
        for size in range(1, 7):
            for order in permutations(range(1, size + 1)):
                raw_input, expected = build_case(order)
                for filename, module in self.modules.items():
                    with self.subTest(size=size, order=order, filename=filename):
                        self.assertEqual(module.solve(raw_input), expected)

    def test_command_line_smoke(self) -> None:
        raw_input, expected = build_case((2, 1, 5, 3, 4))
        result = subprocess.run(
            [sys.executable, str(BASE_DIR / "question-10062-su.py")],
            input=raw_input,
            text=True,
            capture_output=True,
            check=True,
        )
        self.assertEqual(result.stdout.strip(), expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
