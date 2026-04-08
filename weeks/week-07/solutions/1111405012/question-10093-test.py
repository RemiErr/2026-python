from __future__ import annotations

import importlib.util
from pathlib import Path
import subprocess
import sys
import unittest


BASE_DIR = Path(__file__).resolve().parent
SOURCE_FILES = [
    "question-10093.py",
    "question-10093-easy.py",
    "question-10093-su.py",
]


def load_module(filename: str):
    path = BASE_DIR / filename
    module_name = filename.replace("-", "_").replace(".", "_")
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def brute_force(grid: list[str]) -> int:
    plains = []
    for row, line in enumerate(grid):
        for col, ch in enumerate(line):
            if ch == "P":
                plains.append((row, col))

    best = 0
    total = len(plains)
    for mask in range(1 << total):
        positions: list[tuple[int, int]] = []
        ok = True
        for index in range(total):
            if not (mask & (1 << index)):
                continue
            row, col = plains[index]
            for old_row, old_col in positions:
                same_row = row == old_row and abs(col - old_col) <= 2
                same_col = col == old_col and abs(row - old_row) <= 2
                if same_row or same_col:
                    ok = False
                    break
            if not ok:
                break
            positions.append((row, col))
        if ok:
            best = max(best, len(positions))

    return best


class Question10093Tests(unittest.TestCase):
    """用小地圖暴力枚舉，確認 DP 結果正確。"""

    @classmethod
    def setUpClass(cls) -> None:
        cls.modules = {name: load_module(name) for name in SOURCE_FILES}

    def test_all_terrain_patterns_on_3x3(self) -> None:
        height = 3
        width = 3
        for terrain_mask in range(1 << (height * width)):
            grid = []
            for row in range(height):
                chars = []
                for col in range(width):
                    bit = row * width + col
                    chars.append("H" if terrain_mask & (1 << bit) else "P")
                grid.append("".join(chars))

            raw_input = "\n".join([f"{height} {width}"] + grid) + "\n"
            expected = str(brute_force(grid))

            for filename, module in self.modules.items():
                with self.subTest(mask=terrain_mask, filename=filename):
                    self.assertEqual(module.solve(raw_input), expected)

    def test_command_line_smoke(self) -> None:
        raw_input = "3 4\nPPPP\nPHPP\nPPHP\n"
        expected = str(brute_force(["PPPP", "PHPP", "PPHP"]))
        result = subprocess.run(
            [sys.executable, str(BASE_DIR / "question-10093-su.py")],
            input=raw_input,
            text=True,
            capture_output=True,
            check=True,
        )
        self.assertEqual(result.stdout.strip(), expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
