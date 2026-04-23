import contextlib
import importlib.util
import io
import tempfile
import unittest
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent


def load_module(filename, module_name):
    """用檔案路徑載入模組，讓帶有連字號的檔名也能測。"""
    module_path = BASE_DIR / filename
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"無法載入模組：{module_path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


MODULES = {
    "base": load_module("u03-bytes-and-encoding.py", "u03_base"),
    "easy": load_module("u03-bytes-and-encoding-easy.py", "u03_easy"),
    "su": load_module("u03-bytes-and-encoding-su.py", "u03_su"),
}


class TestBytesAndEncoding(unittest.TestCase):
    # 三個版本都跑同一組測試，確保教材版與簡化版結果一致。

    def test_write_and_read_fake_png(self):
        for name, module in MODULES.items():
            with self.subTest(version=name):
                with tempfile.TemporaryDirectory() as temp_dir:
                    fake_png_path = Path(temp_dir) / "fake.png"
                    module.write_fake_png(fake_png_path)
                    head = module.read_head_bytes(fake_png_path)
                    self.assertEqual(head, module.PNG_MAGIC)
                    self.assertTrue(module.bytes_match_png_magic(head))

    def test_first_bytes_as_numbers(self):
        expected = [(137, "0x89"), (80, "0x50"), (78, "0x4e"), (71, "0x47")]
        for name, module in MODULES.items():
            with self.subTest(version=name):
                self.assertEqual(module.first_bytes_as_numbers(module.PNG_MAGIC), expected)

    def test_text_and_bytes_conversion(self):
        for name, module in MODULES.items():
            with self.subTest(version=name):
                data = module.text_to_bytes("你好")
                self.assertIsInstance(data, bytes)
                self.assertEqual(module.bytes_to_text(data), "你好")

    def test_write_and_read_utf8_text(self):
        for name, module in MODULES.items():
            with self.subTest(version=name):
                with tempfile.TemporaryDirectory() as temp_dir:
                    zh_path = Path(temp_dir) / "zh.txt"
                    module.write_utf8_text(zh_path, "中文測試\n")
                    self.assertEqual(module.read_text_with_encoding(zh_path), "中文測試\n")

    def test_wrong_encoding_returns_error_info(self):
        for name, module in MODULES.items():
            with self.subTest(version=name):
                with tempfile.TemporaryDirectory() as temp_dir:
                    zh_path = Path(temp_dir) / "zh.txt"
                    module.write_utf8_text(zh_path, "中文測試\n")
                    result = module.try_read_text(zh_path, "big5")
                    self.assertFalse(result["ok"])
                    self.assertIsInstance(result["value"], str)
                    self.assertTrue(result["value"])

    def test_run_examples(self):
        for name, module in MODULES.items():
            with self.subTest(version=name):
                with tempfile.TemporaryDirectory() as temp_dir:
                    buffer = io.StringIO()
                    with contextlib.redirect_stdout(buffer):
                        module.run_examples(temp_dir)

                    output = buffer.getvalue()
                    self.assertIn("b'\\x89PNG", output)
                    self.assertIn("True", output)
                    self.assertIn("中文測試", output)
                    self.assertIn("解碼錯誤:", output)

                    self.assertTrue((Path(temp_dir) / "fake.png").exists())
                    self.assertTrue((Path(temp_dir) / "zh.txt").exists())


if __name__ == "__main__":
    unittest.main()
