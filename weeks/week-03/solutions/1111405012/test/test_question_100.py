import io
import sys
import unittest
import importlib.util
from pathlib import Path

# 單元測試目標：UVA 100 (3n+1 Problem)
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
        base / "QUESTION-100-su.py",
        base / "QUESTION-100-easy.py",
        base / "uva_100.py",
        base / "solution_100.py",
        base / "uva100.py",
        base / "c039.py",
    ]
    for path in candidates:
        if path.exists():
            return path

    # 其次嘗試 solutions 子目錄中含 100 / uva100 / c039 的檔案
    solutions_dir = base
    if solutions_dir.exists():
        found = []
        for path in solutions_dir.rglob("*.py"):
            name = path.name.lower()
            if name.startswith("test_"):
                continue
            if ("100" in name) or ("uva100" in name) or ("c039" in name):
                found.append(path)
        if found:
            return sorted(found)[0]

    # 如果都找不到，就回傳第一個候選，方便顯示錯誤訊息
    return candidates[0]


def _load_solution_module():
    path = _find_solution_path()
    if not path.exists():
        raise AssertionError(
            "找不到 UVA 100 的解法檔案。\n"
            "請將解法放在 weeks/week-03/ 內，或放在 weeks/week-03/solutions/<student-id>/ 下，\n"
            "檔名建議包含 100 / uva100 / c039，例如 uva_100.py。"
        )

    spec = importlib.util.spec_from_file_location("uva100_solution", path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"無法載入解法檔案：{path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _normalize_output(text: str) -> str:
    """統一輸出格式：去除行尾空白、保留行順序。"""
    lines = [line.rstrip() for line in text.strip().splitlines()]
    return "\n".join(lines)


def _run_solution(input_str: str) -> str:
    module = _load_solution_module()

    if hasattr(module, "solve"):
        out = module.solve(input_str)
        if not isinstance(out, str):
            raise AssertionError("solve() 應回傳字串")
        return _normalize_output(out)

    if hasattr(module, "main"):
        old_stdin, old_stdout = sys.stdin, sys.stdout
        try:
            sys.stdin = io.StringIO(input_str)
            sys.stdout = io.StringIO()
            module.main()
            return _normalize_output(sys.stdout.getvalue())
        finally:
            sys.stdin, sys.stdout = old_stdin, old_stdout

    raise AssertionError("解法模組必須提供 solve(input_str) 或 main() 函式")


class TestUVA100(unittest.TestCase):
    """UVA 100：確認最大 cycle-length 的結果是否正確。"""

    def test_sample_input(self):
        # 題目提供的標準範例
        input_str = "\n".join(
            [
                "1 10",
                "100 200",
                "201 210",
                "900 1000",
            ]
        )
        expected = "\n".join(
            [
                "1 10 20",
                "100 200 125",
                "201 210 89",
                "900 1000 174",
            ]
        )
        self.assertEqual(_run_solution(input_str), expected)

    def test_reverse_range(self):
        # i > j 時仍需輸出原始 i, j 並計算區間最大值
        input_str = "10 1"
        expected = "10 1 20"
        self.assertEqual(_run_solution(input_str), expected)

    def test_single_value(self):
        # i = j 的情況
        input_str = "1 1"
        expected = "1 1 1"
        self.assertEqual(_run_solution(input_str), expected)

    def test_known_cycle_length(self):
        # 題目敘述：22 的 cycle-length 為 16
        input_str = "22 22"
        expected = "22 22 16"
        self.assertEqual(_run_solution(input_str), expected)

    def test_whitespace_and_blank_lines(self):
        # 允許前後空白與空行
        input_str = "  1 10\n\n   100 200   \n"
        expected = "\n".join(["1 10 20", "100 200 125"])
        self.assertEqual(_run_solution(input_str), expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
