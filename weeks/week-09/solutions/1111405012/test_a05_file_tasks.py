import contextlib
import importlib.util
import io
import tempfile
import unittest
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent


def load_module(filename, module_name):
    """用檔案路徑載入模組，讓帶有連字號的檔名也能直接測試。"""
    module_path = BASE_DIR / filename
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"無法載入模組：{module_path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


MODULES = {
    "base": load_module("a05-file-tasks.py", "a05_base"),
    "easy": load_module("a05-file-tasks-easy.py", "a05_easy"),
    "su": load_module("a05-file-tasks-su.py", "a05_su"),
}


class TestA05FileTasks(unittest.TestCase):
    # 三個版本都應該符合相同行為，這樣教材版與簡化版才一致。

    def test_create_diary_once_only(self):
        for name, module in MODULES.items():
            with self.subTest(version=name):
                with tempfile.TemporaryDirectory() as temp_dir:
                    first = module.create_diary(temp_dir, day="2026-04-23")
                    second = module.create_diary(temp_dir, day="2026-04-23")

                    diary_path = Path(temp_dir) / "diary-2026-04-23.txt"
                    self.assertTrue(first["created"])
                    self.assertFalse(second["created"])
                    self.assertTrue(diary_path.exists())
                    self.assertIn("已建立", first["message"])
                    self.assertIn("今天已寫過", second["message"])

    def test_count_py(self):
        expected = (8, 6, 2)
        for name, module in MODULES.items():
            with self.subTest(version=name):
                with tempfile.TemporaryDirectory() as temp_dir:
                    temp_path = Path(temp_dir)
                    (temp_path / "a.py").write_text("def one():\n    pass\n\n# note\n", encoding="utf-8")
                    (temp_path / "sub").mkdir()
                    (temp_path / "sub" / "b.py").write_text("x = 1\n\ndef two():\n    return x\n", encoding="utf-8")
                    self.assertEqual(module.count_py(temp_path), expected)

    def test_format_stats(self):
        expected = [
            "demo",
            "  總行數       : 10",
            "  非空白行     : 8",
            "  def 起頭行數 : 2",
        ]
        for name, module in MODULES.items():
            with self.subTest(version=name):
                self.assertEqual(module.format_stats("demo", (10, 8, 2)), expected)

    def test_run_examples(self):
        for name, module in MODULES.items():
            with self.subTest(version=name):
                with tempfile.TemporaryDirectory() as temp_dir:
                    temp_path = Path(temp_dir)
                    target = temp_path / "stats"
                    target.mkdir()
                    (target / "demo.py").write_text("def hi():\n    return 1\n", encoding="utf-8")

                    buffer = io.StringIO()
                    with contextlib.redirect_stdout(buffer):
                        module.run_examples(temp_path, target_folder=target, day="2026-04-23")

                    output = buffer.getvalue()
                    self.assertIn("已建立 diary-2026-04-23.txt", output)
                    self.assertIn("總行數", output)
                    self.assertIn("def 起頭行數", output)


if __name__ == "__main__":
    unittest.main()
