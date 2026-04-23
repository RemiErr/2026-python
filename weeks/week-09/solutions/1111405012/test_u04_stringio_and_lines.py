import contextlib
import importlib.util
import io
import tempfile
import unittest
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent


def load_module(filename, module_name):
    """用檔案路徑載入模組，讓連字號檔名也能直接測試。"""
    module_path = BASE_DIR / filename
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"無法載入模組：{module_path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


MODULES = {
    "base": load_module("u04-stringio-and-lines.py", "u04_base"),
    "easy": load_module("u04-stringio-and-lines-easy.py", "u04_easy"),
    "su": load_module("u04-stringio-and-lines-su.py", "u04_su"),
}


class TestStringIoAndLines(unittest.TestCase):
    # 三個版本都必須符合相同行為，這樣教材內容才一致。

    def test_build_string_buffer_and_get_text(self):
        expected = "第一行\n第二行\n第三行\n"
        for name, module in MODULES.items():
            with self.subTest(version=name):
                buffer = module.build_string_buffer()
                self.assertEqual(module.get_buffer_text(buffer), expected)

    def test_read_buffer_lines_with_numbers(self):
        expected = [(1, "第一行"), (2, "第二行"), (3, "第三行")]
        for name, module in MODULES.items():
            with self.subTest(version=name):
                buffer = module.build_string_buffer()
                self.assertEqual(module.read_buffer_lines_with_numbers(buffer), expected)

    def test_create_csv_in_memory(self):
        expected = ["name,score", "alice,90"]
        for name, module in MODULES.items():
            with self.subTest(version=name):
                csv_text = module.create_csv_in_memory([["name", "score"], ["alice", 90]])
                self.assertEqual(csv_text.splitlines(), expected)

    def test_write_poem_file(self):
        expected = "床前明月光\n\n疑是地上霜\n\n舉頭望明月\n低頭思故鄉\n"
        for name, module in MODULES.items():
            with self.subTest(version=name):
                with tempfile.TemporaryDirectory() as temp_dir:
                    poem_path = Path(temp_dir) / "poem.txt"
                    module.write_poem_file(poem_path)
                    self.assertEqual(poem_path.read_text(encoding="utf-8"), expected)

    def test_number_nonempty_lines(self):
        expected = "01. 床前明月光\n02. 疑是地上霜\n03. 舉頭望明月\n04. 低頭思故鄉\n"
        for name, module in MODULES.items():
            with self.subTest(version=name):
                with tempfile.TemporaryDirectory() as temp_dir:
                    temp_path = Path(temp_dir)
                    src_path = module.write_poem_file(temp_path / "poem.txt")
                    dst_path = module.number_nonempty_lines(src_path, temp_path / "poem_numbered.txt")
                    self.assertEqual(dst_path.read_text(encoding="utf-8"), expected)

    def test_run_examples(self):
        for name, module in MODULES.items():
            with self.subTest(version=name):
                with tempfile.TemporaryDirectory() as temp_dir:
                    buffer = io.StringIO()
                    with contextlib.redirect_stdout(buffer):
                        module.run_examples(temp_dir)

                    output = buffer.getvalue()
                    self.assertIn("---StringIO 內容---", output)
                    self.assertIn("---CSV in memory---", output)
                    self.assertIn("---加行號後---", output)
                    self.assertIn("01. 床前明月光", output)

                    self.assertTrue((Path(temp_dir) / "poem.txt").exists())
                    self.assertTrue((Path(temp_dir) / "poem_numbered.txt").exists())


if __name__ == "__main__":
    unittest.main()
