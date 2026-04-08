from __future__ import annotations

import importlib.util
from itertools import product
from pathlib import Path
import subprocess
import sys
import unittest


BASE_DIR = Path(__file__).resolve().parent
SOURCE_FILES = [
    "question-10101.py",
    "question-10101-easy.py",
    "question-10101-su.py",
]
MASKS = (
    0b1111110,
    0b0110000,
    0b1101101,
    0b1111001,
    0b0110011,
    0b1011011,
    0b1011111,
    0b1110000,
    0b1111111,
    0b1111011,
)
MASK_TO_DIGIT = {mask: str(index) for index, mask in enumerate(MASKS)}


def load_module(filename: str):
    path = BASE_DIR / filename
    module_name = filename.replace("-", "_").replace(".", "_")
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def evaluate_side(text: str) -> int:
    total = 0
    number = ""
    sign = 1
    index = 0
    if text and text[0] in "+-":
        sign = -1 if text[0] == "-" else 1
        index = 1
    while index <= len(text):
        if index == len(text) or text[index] in "+-":
            total += sign * int(number)
            if index < len(text):
                sign = 1 if text[index] == "+" else -1
            number = ""
            index += 1
            continue
        number += text[index]
        index += 1
    return total


def is_true_equation(expr_with_hash: str) -> bool:
    expr = expr_with_hash.split("#", 1)[0]
    left, right = expr.split("=")
    return evaluate_side(left) == evaluate_side(right)


def same_shape(original: str, changed: str) -> bool:
    left = original.split("#", 1)[0]
    right = changed.split("#", 1)[0]
    if len(left) != len(right):
        return False
    for old_ch, new_ch in zip(left, right):
        if old_ch.isdigit() != new_ch.isdigit():
            return False
        if not old_ch.isdigit() and old_ch != new_ch:
            return False
    return changed.endswith("#")


def brute_force_solutions(expr_with_hash: str) -> set[str]:
    expr = expr_with_hash.split("#", 1)[0]
    digits = [index for index, ch in enumerate(expr) if ch.isdigit()]
    solutions: set[str] = set()

    for source in digits:
        source_mask = MASKS[int(expr[source])]
        for segment_out in range(7):
            if not (source_mask & (1 << segment_out)):
                continue
            source_after = source_mask ^ (1 << segment_out)

            for target in digits:
                target_mask = MASKS[int(expr[target])]
                for segment_in in range(7):
                    if target_mask & (1 << segment_in):
                        continue
                    if source == target and segment_out == segment_in:
                        continue

                    chars = list(expr)
                    if source == target:
                        new_mask = source_after | (1 << segment_in)
                        if new_mask not in MASK_TO_DIGIT:
                            continue
                        chars[source] = MASK_TO_DIGIT[new_mask]
                    else:
                        if source_after not in MASK_TO_DIGIT:
                            continue
                        target_after = target_mask | (1 << segment_in)
                        if target_after not in MASK_TO_DIGIT:
                            continue
                        chars[source] = MASK_TO_DIGIT[source_after]
                        chars[target] = MASK_TO_DIGIT[target_after]

                    candidate = "".join(chars) + "#"
                    if is_true_equation(candidate):
                        solutions.add(candidate)

    return solutions


class Question10101Tests(unittest.TestCase):
    """確認輸出的式子真的能靠移動一根火柴變成正確等式。"""

    @classmethod
    def setUpClass(cls) -> None:
        cls.modules = {name: load_module(name) for name in SOURCE_FILES}

    def assert_valid_result(self, original: str, result: str) -> None:
        solutions = brute_force_solutions(original)
        if result == "No":
            self.assertFalse(solutions, msg=f"{original} 其實有解")
            return
        self.assertTrue(solutions, msg=f"{original} 應該無解，卻輸出 {result}")
        self.assertTrue(same_shape(original, result))
        self.assertTrue(is_true_equation(result))
        self.assertIn(result, solutions)

    def test_all_false_one_digit_equations(self) -> None:
        for a, b, c in product(range(10), repeat=3):
            for op in ["+", "-"]:
                expr = f"{a}{op}{b}={c}#"
                if is_true_equation(expr):
                    continue
                for filename, module in self.modules.items():
                    with self.subTest(expr=expr, filename=filename):
                        self.assert_valid_result(expr, module.solve(expr))

    def test_ignore_text_after_hash(self) -> None:
        expr = "9=6#this-part-should-be-ignored"
        for filename, module in self.modules.items():
            with self.subTest(filename=filename):
                self.assert_valid_result("9=6#", module.solve(expr))

    def test_command_line_smoke(self) -> None:
        result = subprocess.run(
            [sys.executable, str(BASE_DIR / "question-10101-su.py")],
            input="9=6#\n",
            text=True,
            capture_output=True,
            check=True,
        )
        self.assert_valid_result("9=6#", result.stdout.strip())


if __name__ == "__main__":
    unittest.main(verbosity=2)
