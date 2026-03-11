import io
import sys
import unittest
import importlib.util
from pathlib import Path

# 單元測試目標：UVA 490 (Rotating Sentences)
# 期望解法模組提供：
# 1) solve(input_str: str) -> str
# 或
# 2) main() 讀取 stdin、輸出到 stdout


def _find_solution_path() -> Path:
    """在 week-03 中尋找可能的解法檔案。"""
    # test/ 底下的檔案，往上一層才是 solutions/1111405012
    base = Path(__file__).resolve().parent.parent

    # 優先嘗試固定檔名（可自行調整為你實作的檔名）
    candidates = [
        base / "QUESTION-490-su.py",
        base / "QUESTION-490-easy.py",
        base / "uva_490.py",
        base / "solution_490.py",
        base / "uva490.py",
        base / "c045.py",
    ]
    for path in candidates:
        if path.exists():
            return path

    # 其次嘗試 solutions 子目錄中含 490 / uva490 / c045 的檔案
    solutions_dir = base
    if solutions_dir.exists():
        found = []
        for path in solutions_dir.rglob("*.py"):
            name = path.name.lower()
            if name.startswith("test_"):
                continue
            if ("490" in name) or ("uva490" in name) or ("c045" in name):
                found.append(path)
        if found:
            return sorted(found)[0]

    # 如果都找不到，就回傳第一個候選，方便顯示錯誤訊息
    return candidates[0]


def _load_solution_module():
    path = _find_solution_path()
    if not path.exists():
        raise AssertionError(
            "找不到 UVA 490 的解法檔案。\n"
            "請將解法放在 weeks/week-03/ 內，或放在 weeks/week-03/solutions/<student-id>/ 下，\n"
            "檔名建議包含 490 / uva490 / c045，例如 uva_490.py。"
        )

    spec = importlib.util.spec_from_file_location("uva490_solution", path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"無法載入解法檔案：{path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _run_solution(input_str: str) -> str:
    module = _load_solution_module()

    if hasattr(module, "solve"):
        out = module.solve(input_str)
        if not isinstance(out, str):
            raise AssertionError("solve() 應回傳字串")
        return out

    if hasattr(module, "main"):
        old_stdin, old_stdout = sys.stdin, sys.stdout
        try:
            sys.stdin = io.StringIO(input_str)
            sys.stdout = io.StringIO()
            module.main()
            return sys.stdout.getvalue()
        finally:
            sys.stdin, sys.stdout = old_stdin, old_stdout

    raise AssertionError("解法模組必須提供 solve(input_str) 或 main() 函式")


class TestUVA490(unittest.TestCase):
    """UVA 490：確認文字矩陣順時針旋轉 90 度。"""

    def test_basic_two_lines(self):
        # 兩行基本案例
        input_str = "HELLO\nWORLD\n"
        expected = "WH\nOE\nRL\nLL\nDO\n"
        self.assertEqual(_run_solution(input_str), expected)

    def test_varying_lengths(self):
        # 不同行長，需補空白形成矩形
        input_str = "ABCD\nEF\nGHI\n"
        expected = "GEA\nHFB\nI C\n  D\n"
        self.assertEqual(_run_solution(input_str), expected)

    def test_single_line(self):
        # 只有一行時，旋轉後為直向輸出
        input_str = "ABC\n"
        expected = "A\nB\nC\n"
        self.assertEqual(_run_solution(input_str), expected)

    def test_lines_with_spaces(self):
        # 含空白字元（須保留空白）
        input_str = "A B\nCD \n"
        expected = "CA\nD\n B\n"
        self.assertEqual(_run_solution(input_str), expected)

    def test_trailing_newline_optional(self):
        # 沒有結尾換行也應可處理
        input_str = "XY\nZ"
        expected = "ZX\n Y\n"
        self.assertEqual(_run_solution(input_str), expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
