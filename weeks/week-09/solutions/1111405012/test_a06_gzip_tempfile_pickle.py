import contextlib
import importlib.util
import io
import tempfile
import unittest
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent


def load_module(filename, module_name):
    """用檔案路徑載入模組，讓連字號檔名也能直接測。"""
    module_path = BASE_DIR / filename
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"無法載入模組：{module_path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


MODULES = {
    "base": load_module("a06-gzip-tempfile-pickle.py", "a06_base"),
    "easy": load_module("a06-gzip-tempfile-pickle-easy.py", "a06_easy"),
    "su": load_module("a06-gzip-tempfile-pickle-su.py", "a06_su"),
}


class TestA06GzipTempfilePickle(unittest.TestCase):
    # 每個版本都跑相同測試，確保教學版與簡化版行為一致。

    def test_gzip_text_roundtrip(self):
        expected = ["第一行筆記", "第二行筆記"]
        for name, module in MODULES.items():
            with self.subTest(version=name):
                with tempfile.TemporaryDirectory() as temp_dir:
                    path = Path(temp_dir) / "notes.txt.gz"
                    module.write_gzip_text(path, expected)
                    self.assertEqual(module.read_gzip_lines(path), expected)

    def test_gzip_bytes_roundtrip(self):
        expected = b"\x00\x01\x02\x03"
        for name, module in MODULES.items():
            with self.subTest(version=name):
                with tempfile.TemporaryDirectory() as temp_dir:
                    path = Path(temp_dir) / "blob.bin.gz"
                    module.write_gzip_bytes(path, expected)
                    self.assertEqual(module.read_gzip_bytes(path), expected)
                    self.assertGreater(module.path_size(path), 0)

    def test_temporary_directory_cleanup(self):
        expected = {"a.txt": "hello", "b.txt": "world"}
        for name, module in MODULES.items():
            with self.subTest(version=name):
                result = module.demo_temporary_directory()
                self.assertEqual(result["files"], expected)
                self.assertFalse(result["exists_after"])

    def test_named_temporary_file_cleanup(self):
        for name, module in MODULES.items():
            with self.subTest(version=name):
                result = module.demo_named_temporary_file()
                self.assertTrue(result["exists_before_delete"])
                self.assertFalse(result["exists_after_delete"])
                self.assertEqual(result["content"], "暫存 log\n")

    def test_pickle_roundtrip(self):
        scores = {"alice": [90, 85, 92], "bob": [70, 75, 80], "carol": [88, 91, 95]}
        for name, module in MODULES.items():
            with self.subTest(version=name):
                with tempfile.TemporaryDirectory() as temp_dir:
                    path = Path(temp_dir) / "scores.pkl"
                    module.dump_pickle(path, scores)
                    loaded = module.load_pickle(path)
                    self.assertEqual(loaded, scores)
                    self.assertEqual(module.alice_average(loaded), 89.0)

    def test_run_examples(self):
        for name, module in MODULES.items():
            with self.subTest(version=name):
                with tempfile.TemporaryDirectory() as temp_dir:
                    buffer = io.StringIO()
                    with contextlib.redirect_stdout(buffer):
                        module.run_examples(temp_dir)

                    output = buffer.getvalue()
                    self.assertIn("gz: 第一行筆記", output)
                    self.assertIn("blob size:", output)
                    self.assertIn("離開後還存在嗎？ False", output)
                    self.assertIn("alice 平均: 89.0", output)

                    self.assertTrue((Path(temp_dir) / "notes.txt.gz").exists())
                    self.assertTrue((Path(temp_dir) / "blob.bin.gz").exists())
                    self.assertTrue((Path(temp_dir) / "scores.pkl").exists())


if __name__ == "__main__":
    unittest.main()
