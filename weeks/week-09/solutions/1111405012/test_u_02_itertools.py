import contextlib
import importlib.util
import io
import unittest
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent


def load_module(filename, module_name):
    """用檔案路徑載入模組，讓檔名帶有 -easy / -su 也能直接測。"""
    module_path = BASE_DIR / filename
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"無法載入模組：{module_path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


MODULES = {
    "base": load_module("u_02_itertools.py", "u02_base"),
    "easy": load_module("u_02_itertools-easy.py", "u02_easy"),
    "su": load_module("u_02_itertools-su.py", "u02_su"),
}


class TestItertoolsExamples(unittest.TestCase):
    # 每個版本都跑同樣的測試，確保教材版、easy 版、su 版結果一致。

    def test_count_generator(self):
        expected = [3, 4, 5, 6]
        for name, module in MODULES.items():
            with self.subTest(version=name):
                counter = module.count(3)
                result = [next(counter) for _ in range(4)]
                self.assertEqual(result, expected)

    def test_slice_count(self):
        expected = [5, 6, 7, 8, 9]
        for name, module in MODULES.items():
            with self.subTest(version=name):
                self.assertEqual(module.slice_count(0, 5, 10), expected)

    def test_drop_until_limit(self):
        expected = [5, 2, 4, 6]
        nums = [1, 3, 5, 2, 4, 6]
        for name, module in MODULES.items():
            with self.subTest(version=name):
                self.assertEqual(module.drop_until_limit(nums, 5), expected)

    def test_take_until_limit(self):
        expected = [1, 3]
        nums = [1, 3, 5, 2, 4, 6]
        for name, module in MODULES.items():
            with self.subTest(version=name):
                self.assertEqual(module.take_until_limit(nums, 5), expected)

    def test_chain_values(self):
        expected = [1, 2, 3, 4, 5]
        for name, module in MODULES.items():
            with self.subTest(version=name):
                self.assertEqual(module.chain_values([1, 2], [3, 4], [5]), expected)

    def test_get_permutations(self):
        expected = [
            ("a", "b", "c"),
            ("a", "c", "b"),
            ("b", "a", "c"),
            ("b", "c", "a"),
            ("c", "a", "b"),
            ("c", "b", "a"),
        ]
        for name, module in MODULES.items():
            with self.subTest(version=name):
                self.assertEqual(module.get_permutations(["a", "b", "c"]), expected)

    def test_get_permutations_with_length(self):
        expected = [
            ("a", "b"),
            ("a", "c"),
            ("b", "a"),
            ("b", "c"),
            ("c", "a"),
            ("c", "b"),
        ]
        for name, module in MODULES.items():
            with self.subTest(version=name):
                self.assertEqual(module.get_permutations(["a", "b", "c"], 2), expected)

    def test_get_combinations(self):
        expected = [("a", "b"), ("a", "c"), ("b", "c")]
        for name, module in MODULES.items():
            with self.subTest(version=name):
                self.assertEqual(module.get_combinations(["a", "b", "c"], 2), expected)

    def test_password_candidates(self):
        expected = ["AB", "A1", "BA", "B1", "1A", "1B"]
        for name, module in MODULES.items():
            with self.subTest(version=name):
                self.assertEqual(module.password_candidates(["A", "B", "1"]), expected)

    def test_repeated_password_candidates(self):
        expected = ["AA", "AB", "A1", "BB", "B1", "11"]
        for name, module in MODULES.items():
            with self.subTest(version=name):
                self.assertEqual(module.repeated_password_candidates(["A", "B", "1"]), expected)

    def test_run_examples(self):
        for name, module in MODULES.items():
            with self.subTest(version=name):
                buffer = io.StringIO()
                with contextlib.redirect_stdout(buffer):
                    module.run_examples()
                output = buffer.getvalue()
                self.assertIn("islice(c, 5, 10): [5, 6, 7, 8, 9]", output)
                self.assertIn("2位數密碼:", output)
                self.assertIn("2位數密碼（可重複）:", output)


if __name__ == "__main__":
    unittest.main()
