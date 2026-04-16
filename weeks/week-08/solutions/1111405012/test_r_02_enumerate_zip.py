"""測試 enumerate() 與 zip() 教材版本。"""

import importlib.util
import unittest
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent


def load_module(filename, module_name):
    # 透過檔案路徑載入不同版本。
    spec = importlib.util.spec_from_file_location(module_name, BASE_DIR / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


MODULES = [
    load_module("r_02_enumerate_zip.py", "r02_main"),
    load_module("r_02_enumerate_zip-easy.py", "r02_easy"),
    load_module("r_02_enumerate_zip-su.py", "r02_su"),
]


EXPECTED_RENDER = "\n".join(
    [
        "enumerate() 和 zip() 範例",
        "enumerate(colors): [(0, 'red'), (1, 'green'), (2, 'blue')]",
        "enumerate(colors, 1): [(1, 'red'), (2, 'green'), (3, 'blue')]",
        "行號: [(1, 'line1'), (2, 'line2'), (3, 'line3')]",
        "配對姓名分數: [('Alice', 90), ('Bob', 85), ('Carol', 92)]",
        "三個串列相加: [111, 222, 333]",
        "zip 最短配對: [(1, 'a'), (2, 'b')]",
        "zip_longest 配對: [(1, 'a'), (2, 'b'), (0, 'c')]",
        "建立字典: {'name': 'John', 'age': '30', 'city': 'NYC'}",
    ]
)


class TestEnumerateZip(unittest.TestCase):
    def test_enumerate_examples(self):
        # enumerate() 的索引與內容都應正確。
        for module in MODULES:
            with self.subTest(module=module.__name__):
                self.assertEqual(
                    module.enumerate_colors(["red", "green", "blue"]),
                    [(0, "red"), (1, "green"), (2, "blue")],
                )
                self.assertEqual(
                    module.enumerate_colors(["red", "green", "blue"], 1),
                    [(1, "red"), (2, "green"), (3, "blue")],
                )
                self.assertEqual(
                    module.number_lines(["line1", "line2", "line3"]),
                    [(1, "line1"), (2, "line2"), (3, "line3")],
                )

    def test_zip_examples(self):
        # zip() 與 zip_longest() 的行為都要一致。
        for module in MODULES:
            with self.subTest(module=module.__name__):
                self.assertEqual(
                    module.pair_names_scores(["Alice", "Bob", "Carol"], [90, 85, 92]),
                    [("Alice", 90), ("Bob", 85), ("Carol", 92)],
                )
                self.assertEqual(
                    module.sum_three_lists([1, 2, 3], [10, 20, 30], [100, 200, 300]),
                    [111, 222, 333],
                )
                self.assertEqual(module.zip_shortest([1, 2], ["a", "b", "c"]), [(1, "a"), (2, "b")])
                self.assertEqual(
                    module.zip_with_fill([1, 2], ["a", "b", "c"]),
                    [(1, "a"), (2, "b"), (0, "c")],
                )

    def test_make_dict(self):
        # dict(zip()) 要能建立完整對照表。
        expected = {"name": "John", "age": "30", "city": "NYC"}
        for module in MODULES:
            with self.subTest(module=module.__name__):
                self.assertEqual(
                    module.make_dict(["name", "age", "city"], ["John", "30", "NYC"]),
                    expected,
                )

    def test_render_demo(self):
        # 展示文字要維持一致。
        for module in MODULES:
            with self.subTest(module=module.__name__):
                self.assertEqual(module.render_demo(), EXPECTED_RENDER)


if __name__ == "__main__":
    unittest.main()
