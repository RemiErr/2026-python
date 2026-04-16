"""測試生成器教材版本。"""

import importlib.util
import unittest
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent


def load_module(filename, module_name):
    # 這裡使用檔案路徑，方便載入不同檔名格式。
    spec = importlib.util.spec_from_file_location(module_name, BASE_DIR / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


MODULES = [
    load_module("u_01_generator_basics.py", "u01_main"),
    load_module("u_01_generator_basics-easy.py", "u01_easy"),
    load_module("u_01_generator_basics-su.py", "u01_su"),
]


EXPECTED_RENDER = "\n".join(
    [
        "生成器概念",
        "frange(0, 2, 0.5): [0, 0.5, 1.0, 1.5]",
        "Starting countdown from 3",
        "next(c): 3",
        "next(c): 2",
        "next(c): 1",
        "Done!",
        "StopIteration!",
        "Fibonacci 前 10 個: [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]",
        "chain_iter: [1, 2, 3, 4, 5, 6]",
        "深度優先: [0, 1, 3, 4, 2]",
        "展開: [1, 2, 3, 4, 5]",
    ]
)


class TestGeneratorBasics(unittest.TestCase):
    def test_frange_and_countdown(self):
        # 先確認有限生成器的輸出是否正確。
        for module in MODULES:
            with self.subTest(module=module.__name__):
                self.assertEqual(list(module.frange(0, 2, 0.5)), [0, 0.5, 1.0, 1.5])
                self.assertEqual(list(module.countdown(3)), [3, 2, 1])

    def test_fibonacci_and_chain(self):
        # 無限生成器要只取前 10 個值，並確認串接結果。
        for module in MODULES:
            with self.subTest(module=module.__name__):
                self.assertEqual(module.first_n_fibonacci(10), [0, 1, 1, 2, 3, 5, 8, 13, 21, 34])
                self.assertEqual(list(module.chain_iter([1, 2], [3, 4], [5, 6])), [1, 2, 3, 4, 5, 6])

    def test_tree_and_flatten(self):
        # 樹狀走訪與巢狀展開都要保留原本的教學重點。
        for module in MODULES:
            with self.subTest(module=module.__name__):
                self.assertEqual(module.depth_first_values(module.build_sample_tree()), [0, 1, 3, 4, 2])
                self.assertEqual(list(module.flatten([1, [2, [3, 4]], 5])), [1, 2, 3, 4, 5])

    def test_render_demo(self):
        # 三個版本的展示文字要一致。
        for module in MODULES:
            with self.subTest(module=module.__name__):
                self.assertEqual(module.render_demo(), EXPECTED_RENDER)


if __name__ == "__main__":
    unittest.main()
