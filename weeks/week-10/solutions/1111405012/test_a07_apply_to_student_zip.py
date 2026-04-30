import csv
import importlib.util
import io
import tempfile
import unittest
import zipfile
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parent / "a07-apply-to-student-zip.py"


def load_module():
    """用檔案路徑載入待測模組，避免連字號檔名不能直接 import。"""
    spec = importlib.util.spec_from_file_location("a07_apply_to_student_zip", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def make_zip(zip_path: Path):
    """建立最小可測的學生資料壓縮檔。"""
    cases = {
        "113_students.csv": [
            ["系所名稱", "入學方式", "姓名"],
            ["資訊工程系", "聯合登記分發", "甲"],
            ["電機工程系", "繁星推甄", "乙"],
            ["資訊工程系", "聯合登記分發", "丙"],
        ],
        "114_students.csv": [
            ["系所名稱", "入學方式", "姓名"],
            ["觀光休閒系", "個人申請", "丁"],
            ["資訊工程系", "聯合登記分發", "戊"],
        ],
    }

    with zipfile.ZipFile(zip_path, "w") as archive:
        for filename, rows in cases.items():
            buffer = io.StringIO()
            writer = csv.writer(buffer)
            writer.writerows(rows)
            archive.writestr(filename, buffer.getvalue().encode("utf-8-sig"))


class TestA07ApplyToStudentZip(unittest.TestCase):
    """驗證跨年度 zip 讀取、統計與報告輸出。"""

    def test_iter_year_csv_reads_year_and_rows(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            zip_path = Path(temp_dir) / "students.zip"
            make_zip(zip_path)
            module = load_module()

            cases = list(module.iter_year_csv(zip_path))

            self.assertEqual([year for year, _, _ in cases], ["113", "114"])
            self.assertEqual(cases[0][1], ["系所名稱", "入學方式", "姓名"])
            self.assertEqual(len(cases[0][2]), 3)

    def test_build_summary_counts_department_and_entry(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            zip_path = Path(temp_dir) / "students.zip"
            make_zip(zip_path)
            module = load_module()

            summary, all_depts = module.build_summary(zip_path)

            self.assertEqual(summary["113"]["total"], 3)
            self.assertEqual(summary["113"]["by_dept"]["資訊工程系"], 2)
            self.assertEqual(summary["114"]["by_entry"]["聯合登記分發"], 1)
            self.assertEqual(all_depts["資訊工程系"], 3)

    def test_build_markdown_report_contains_top_department(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            zip_path = Path(temp_dir) / "students.zip"
            make_zip(zip_path)
            module = load_module()
            summary, _ = module.build_summary(zip_path)

            report = module.build_markdown_report(summary)

            self.assertIn("# 6 屆新生概況報告", report)
            self.assertIn("| 113 | 3 | 資訊工程系 (2) |", report)

    def test_save_and_load_snapshot_roundtrip(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            zip_path = Path(temp_dir) / "students.zip"
            snapshot_path = Path(temp_dir) / "summary.pkl"
            make_zip(zip_path)
            module = load_module()
            summary, _ = module.build_summary(zip_path)

            module.save_snapshot(summary, snapshot_path)
            loaded = module.load_snapshot(snapshot_path)

            self.assertEqual(loaded["113"]["total"], 3)
            self.assertEqual(loaded["114"]["by_dept"]["觀光休閒系"], 1)


if __name__ == "__main__":
    unittest.main()
