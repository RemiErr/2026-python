import csv
import importlib.util
import io
import tempfile
import unittest
import zipfile
from pathlib import Path

import matplotlib


matplotlib.use("Agg")

MODULE_PATH = Path(__file__).resolve().parent / "a08-seaborn-college-trend.py"


def load_module():
    """用路徑載入待測模組。"""
    spec = importlib.util.spec_from_file_location("a08_seaborn_college_trend", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def make_zip(zip_path: Path):
    """建立可用來驗證學院對照與年度統計的簡化資料。"""
    cases = {
        "113_students.csv": [
            ["系所名稱"],
            ["資訊工程系"],
            ["電機工程系"],
            ["觀光休閒系"],
        ],
        "114_students.csv": [
            ["系所名稱"],
            ["資訊工程系"],
            ["資訊工程系"],
            ["餐旅管理系"],
        ],
    }

    with zipfile.ZipFile(zip_path, "w") as archive:
        for filename, rows in cases.items():
            buffer = io.StringIO()
            writer = csv.writer(buffer)
            writer.writerows(rows)
            archive.writestr(filename, buffer.getvalue().encode("utf-8-sig"))


class TestA08SeabornCollegeTrend(unittest.TestCase):
    """驗證資料轉 DataFrame、統計與 PNG 圖檔輸出。"""

    def test_load_long_frame_maps_department_to_college(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            zip_path = Path(temp_dir) / "students.zip"
            make_zip(zip_path)
            module = load_module()

            frame = module.load_long_frame(zip_path)

            self.assertEqual(len(frame), 6)
            self.assertIn("學院", frame.columns)
            self.assertIn("電資工程學院", set(frame["學院"]))

    def test_build_year_college_summary_counts_rows(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            zip_path = Path(temp_dir) / "students.zip"
            make_zip(zip_path)
            module = load_module()
            frame = module.load_long_frame(zip_path)

            summary = module.build_year_college_summary(frame)

            row = summary[(summary["學年"] == 114) & (summary["學院"] == "電資工程學院")]
            self.assertEqual(int(row.iloc[0]["人數"]), 2)

    def test_build_figure_returns_two_axes(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            zip_path = Path(temp_dir) / "students.zip"
            make_zip(zip_path)
            module = load_module()
            frame = module.load_long_frame(zip_path)
            summary = module.build_year_college_summary(frame)

            fig = module.build_figure(summary)

            self.assertEqual(len(fig.axes), 2)
            self.assertEqual(fig.axes[0].get_title(), "109–114 各學院新生人數趨勢")
            self.assertEqual(fig.axes[1].get_ylabel(), "人數")
            module.plt.close(fig)

    def test_save_figure_creates_png_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            zip_path = Path(temp_dir) / "students.zip"
            output_path = Path(temp_dir) / "trend.png"
            make_zip(zip_path)
            module = load_module()
            frame = module.load_long_frame(zip_path)
            summary = module.build_year_college_summary(frame)
            fig = module.build_figure(summary)

            created = module.save_figure(fig, output_path)

            self.assertTrue(created)
            self.assertTrue(output_path.exists())
            module.plt.close(fig)


if __name__ == "__main__":
    unittest.main()
