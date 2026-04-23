import contextlib
import importlib.util
import io
import os
import tempfile
import unittest
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent


def load_module(filename, module_name):
    """用檔案路徑載入模組，這樣就能直接測連字號檔名。"""
    module_path = BASE_DIR / filename
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"無法載入模組：{module_path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


MODULES = {
    "base": load_module("r02-path-and-listing.py", "r02_base"),
    "easy": load_module("r02-path-and-listing-easy.py", "r02_easy"),
    "su": load_module("r02-path-and-listing-su.py", "r02_su"),
}


class TestPathAndListing(unittest.TestCase):
    # 測試會同時檢查三個版本，確保教材版與簡化版內容一致。

    def test_build_week_path(self):
        expected = Path("weeks") / "week-09"
        for name, module in MODULES.items():
            with self.subTest(version=name):
                self.assertEqual(module.build_week_path(), expected)

    def test_describe_path(self):
        for name, module in MODULES.items():
            with self.subTest(version=name):
                info = module.describe_path("hello.txt")
                self.assertEqual(info["name"], "hello.txt")
                self.assertEqual(info["stem"], "hello")
                self.assertEqual(info["suffix"], ".txt")

    def test_join_with_os(self):
        expected = os.path.join("weeks", "week-09", "README.md")
        for name, module in MODULES.items():
            with self.subTest(version=name):
                self.assertEqual(module.join_with_os("weeks", "week-09", "README.md"), expected)

    def test_check_path_status(self):
        for name, module in MODULES.items():
            with self.subTest(version=name):
                with tempfile.TemporaryDirectory() as temp_dir:
                    temp_path = Path(temp_dir)
                    file_path = temp_path / "hello.txt"
                    folder_path = temp_path / "data"
                    file_path.write_text("hi", encoding="utf-8")
                    folder_path.mkdir()

                    file_status = module.check_path_status(file_path)
                    folder_status = module.check_path_status(folder_path)

                    self.assertEqual(file_status, {"exists": True, "is_file": True, "is_dir": False})
                    self.assertEqual(folder_status, {"exists": True, "is_file": False, "is_dir": True})

    def test_missing_message(self):
        for name, module in MODULES.items():
            with self.subTest(version=name):
                message = module.missing_message("no_such_file.txt")
                self.assertEqual(message, "no_such_file.txt 不存在，略過讀取")

    def test_list_directory_names(self):
        expected = ["a.py", "b.txt", "folder"]
        for name, module in MODULES.items():
            with self.subTest(version=name):
                with tempfile.TemporaryDirectory() as temp_dir:
                    temp_path = Path(temp_dir)
                    (temp_path / "b.txt").write_text("b", encoding="utf-8")
                    (temp_path / "a.py").write_text("a", encoding="utf-8")
                    (temp_path / "folder").mkdir()
                    self.assertEqual(module.list_directory_names(temp_path), expected)

    def test_glob_py_files(self):
        expected = ["a.py", "c.py"]
        for name, module in MODULES.items():
            with self.subTest(version=name):
                with tempfile.TemporaryDirectory() as temp_dir:
                    temp_path = Path(temp_dir)
                    (temp_path / "a.py").write_text("", encoding="utf-8")
                    (temp_path / "b.txt").write_text("", encoding="utf-8")
                    (temp_path / "c.py").write_text("", encoding="utf-8")
                    self.assertEqual(module.glob_py_files(temp_path), expected)

    def test_rglob_py_files(self):
        expected = ["main.py", "sub/child.py"]
        for name, module in MODULES.items():
            with self.subTest(version=name):
                with tempfile.TemporaryDirectory() as temp_dir:
                    temp_path = Path(temp_dir)
                    (temp_path / "sub").mkdir()
                    (temp_path / "main.py").write_text("", encoding="utf-8")
                    (temp_path / "sub" / "child.py").write_text("", encoding="utf-8")
                    (temp_path / "sub" / "note.txt").write_text("", encoding="utf-8")
                    self.assertEqual(module.rglob_py_files(temp_path), expected)

    def test_first_rglob_py(self):
        for name, module in MODULES.items():
            with self.subTest(version=name):
                with tempfile.TemporaryDirectory() as temp_dir:
                    temp_path = Path(temp_dir)
                    (temp_path / "sub").mkdir()
                    (temp_path / "z.py").write_text("", encoding="utf-8")
                    (temp_path / "sub" / "a.py").write_text("", encoding="utf-8")
                    self.assertEqual(module.first_rglob_py(temp_path), "sub/a.py")

    def test_run_examples(self):
        for name, module in MODULES.items():
            with self.subTest(version=name):
                with tempfile.TemporaryDirectory() as temp_dir:
                    temp_path = Path(temp_dir)
                    (temp_path / "hello.txt").write_text("hello", encoding="utf-8")
                    (temp_path / "demo.py").write_text("print('x')", encoding="utf-8")
                    (temp_path / "sub").mkdir()
                    (temp_path / "sub" / "child.py").write_text("print('y')", encoding="utf-8")

                    buffer = io.StringIO()
                    with contextlib.redirect_stdout(buffer):
                        module.run_examples(temp_path, temp_path)

                    output = buffer.getvalue()
                    self.assertIn("week-09", output)
                    self.assertIn("no_such_file.txt 不存在，略過讀取", output)
                    self.assertIn("listdir:", output)
                    self.assertIn("glob: demo.py", output)
                    self.assertIn("rglob:", output)


if __name__ == "__main__":
    unittest.main()
