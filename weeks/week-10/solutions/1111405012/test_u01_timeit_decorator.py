import importlib.util
import io
import unittest
from contextlib import redirect_stdout
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parent / "u01-timeit-decorator.py"


def load_module():
    """用檔案路徑載入模組，避開連字號檔名的 import 限制。"""
    spec = importlib.util.spec_from_file_location("u01_timeit_decorator", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TestU01TimeitDecorator(unittest.TestCase):
    """驗證三種格式解析、裝飾器 metadata 與基準測試流程。"""

    def setUp(self):
        self.module = load_module()
        self.sample_rows = [
            {"id": 1, "name": "Alice", "score": 88},
            {"id": 2, "name": "Bob", "score": 91},
        ]
        self.csv_data, self.json_data, self.xml_data = self.module.make_sample_data(self.sample_rows)

    def test_read_csv_raw_parses_rows(self):
        result = self.module.read_csv_raw(self.csv_data)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["name"], "Alice")
        self.assertEqual(result[1]["score"], "91")

    def test_read_json_raw_parses_rows(self):
        result = self.module.read_json_raw(self.json_data)
        self.assertEqual(result[0]["id"], 1)
        self.assertEqual(result[1]["name"], "Bob")

    def test_read_xml_raw_parses_rows(self):
        result = self.module.read_xml_raw(self.xml_data)
        self.assertEqual(result[0]["id"], "1")
        self.assertEqual(result[1]["score"], "91")

    def test_timeit_preserves_name_and_doc(self):
        @self.module.timeit
        def demo():
            """示範文件字串"""
            return "ok"

        output = io.StringIO()
        with redirect_stdout(output):
            value = demo()

        self.assertEqual(value, "ok")
        self.assertEqual(demo.__name__, "demo")
        self.assertEqual(demo.__doc__, "示範文件字串")
        self.assertIn("demo", output.getvalue())

    def test_timeit_silent_returns_result_and_elapsed(self):
        wrapped = self.module.timeit_silent(self.module.read_json_raw)
        result, elapsed = wrapped(self.json_data)

        self.assertEqual(len(result), 2)
        self.assertIsInstance(elapsed, float)
        self.assertGreaterEqual(elapsed, 0.0)

    def test_benchmark_formats_returns_average_times(self):
        report = self.module.benchmark_formats(self.csv_data, self.json_data, self.xml_data, runs=2)

        self.assertEqual(set(report.keys()), {"CSV", "JSON", "XML"})
        for value in report.values():
            self.assertIsInstance(value, float)
            self.assertGreaterEqual(value, 0.0)

    def test_format_report_contains_headers(self):
        text = self.module.format_report({"CSV": 0.3, "JSON": 0.1, "XML": 0.5}, record_count=2, runs=3)

        self.assertIn("=== 讀取 2 筆資料，重複 3 次平均 ===", text)
        self.assertIn("格式", text)
        self.assertIn("CSV", text)
        self.assertIn("JSON", text)
        self.assertIn("XML", text)


if __name__ == "__main__":
    unittest.main()
