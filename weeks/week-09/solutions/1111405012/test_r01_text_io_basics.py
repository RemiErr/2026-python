import contextlib
import importlib.util
import io
import tempfile
import unittest
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent


def load_module(filename, module_name):
    """用檔案路徑載入模組，讓帶有連字號的檔名也能測試。"""
    module_path = BASE_DIR / filename
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"無法載入模組：{module_path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


MODULES = {
    "base": load_module("r01-text-io-basics.py", "r01_base"),
    "easy": load_module("r01-text-io-basics-easy.py", "r01_easy"),
    "su": load_module("r01-text-io-basics-su.py", "r01_su"),
}


class TestTextIoBasics(unittest.TestCase):
    # 三個版本都應該通過同一套測試，確保教學內容一致。

    def test_write_and_read_hello_file(self):
        expected_text = "你好，Python\n第二行\n"
        expected_lines = ["你好，Python", "第二行"]

        for name, module in MODULES.items():
            with self.subTest(version=name):
                with tempfile.TemporaryDirectory() as temp_dir:
                    hello_path = Path(temp_dir) / "hello.txt"
                    module.write_hello_file(hello_path)

                    self.assertTrue(hello_path.exists())
                    self.assertEqual(module.read_all_text(hello_path), expected_text)
                    self.assertEqual(module.read_lines(hello_path), expected_lines)

    def test_write_log_file(self):
        expected = "登入成功\n使用者: alice\n"

        for name, module in MODULES.items():
            with self.subTest(version=name):
                with tempfile.TemporaryDirectory() as temp_dir:
                    log_path = Path(temp_dir) / "log.txt"
                    module.write_log_file(log_path)
                    self.assertEqual(log_path.read_text(encoding="utf-8"), expected)

    def test_write_and_append_csv_text(self):
        expected = "apple,banana,cherry\ndate,2026-04-23\n"

        for name, module in MODULES.items():
            with self.subTest(version=name):
                with tempfile.TemporaryDirectory() as temp_dir:
                    csv_path = Path(temp_dir) / "fruits.csv"
                    module.write_fruits_csv(csv_path, ["apple", "banana", "cherry"])
                    module.append_csv_pair(csv_path, "date", "2026-04-23")
                    self.assertEqual(module.read_text_with_path(csv_path), expected)

    def test_text_mode_bytes_error(self):
        for name, module in MODULES.items():
            with self.subTest(version=name):
                with tempfile.TemporaryDirectory() as temp_dir:
                    bad_path = Path(temp_dir) / "bad.txt"
                    message = module.demonstrate_text_mode_type_error(bad_path)
                    self.assertTrue(message)
                    self.assertIsInstance(message, str)

    def test_run_examples(self):
        for name, module in MODULES.items():
            with self.subTest(version=name):
                with tempfile.TemporaryDirectory() as temp_dir:
                    buffer = io.StringIO()
                    with contextlib.redirect_stdout(buffer):
                        module.run_examples(temp_dir)

                    output = buffer.getvalue()
                    self.assertIn("你好，Python", output)
                    self.assertIn("apple,banana,cherry", output)
                    self.assertIn("錯誤示範:", output)

                    self.assertTrue((Path(temp_dir) / "hello.txt").exists())
                    self.assertTrue((Path(temp_dir) / "log.txt").exists())
                    self.assertTrue((Path(temp_dir) / "fruits.csv").exists())


if __name__ == "__main__":
    unittest.main()
