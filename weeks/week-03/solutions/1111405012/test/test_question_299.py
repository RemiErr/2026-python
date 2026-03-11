import io
import sys
import unittest
import importlib.util
from pathlib import Path

# 單元測試目標：UVA 299 (Train Swapping)
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
        base / "QUESTION-299-su.py",
        base / "QUESTION-299-easy.py",
        base / "uva_299.py",
        base / "solution_299.py",
        base / "uva299.py",
        base / "e561.py",
    ]
    for path in candidates:
        if path.exists():
            return path

    # 其次嘗試 solutions 子目錄中含 299 / uva299 / e561 的檔案
    solutions_dir = base
    if solutions_dir.exists():
        found = []
        for path in solutions_dir.rglob("*.py"):
            name = path.name.lower()
            if name.startswith("test_"):
                continue
            if ("299" in name) or ("uva299" in name) or ("e561" in name):
                found.append(path)
        if found:
            return sorted(found)[0]

    # 如果都找不到，就回傳第一個候選，方便顯示錯誤訊息
    return candidates[0]


def _load_solution_module():
    path = _find_solution_path()
    if not path.exists():
        raise AssertionError(
            "找不到 UVA 299 的解法檔案。\n"
            "請將解法放在 weeks/week-03/ 內，或放在 weeks/week-03/solutions/<student-id>/ 下，\n"
            "檔名建議包含 299 / uva299 / e561，例如 uva_299.py。"
        )

    spec = importlib.util.spec_from_file_location("uva299_solution", path)
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


class TestUVA299(unittest.TestCase):
    """UVA 299：確認最少相鄰交換次數。"""

    def test_official_sample(self):
        # UVA 299 標準範例
        input_str = "\n".join(
            [
                "3",
                "3",
                "1 3 2",
                "4",
                "4 3 2 1",
                "2",
                "2 1",
            ]
        )
        expected = "\n".join(
            [
                "Optimal train swapping takes 1 swaps.",
                "Optimal train swapping takes 6 swaps.",
                "Optimal train swapping takes 1 swaps.",
            ]
        )
        self.assertEqual(_run_solution(input_str), expected)

    def test_already_sorted(self):
        # 已經排好順序，交換次數應為 0
        input_str = "\n".join(
            [
                "1",
                "5",
                "1 2 3 4 5",
            ]
        )
        expected = "Optimal train swapping takes 0 swaps."
        self.assertEqual(_run_solution(input_str), expected)

    def test_reverse_sorted(self):
        # 完全反序，交換次數為 L*(L-1)/2
        input_str = "\n".join(
            [
                "1",
                "5",
                "5 4 3 2 1",
            ]
        )
        expected = "Optimal train swapping takes 10 swaps."
        self.assertEqual(_run_solution(input_str), expected)

    def test_length_one(self):
        # 只有一節車廂
        input_str = "\n".join(
            [
                "1",
                "1",
                "1",
            ]
        )
        expected = "Optimal train swapping takes 0 swaps."
        self.assertEqual(_run_solution(input_str), expected)

    def test_whitespace_and_blank_lines(self):
        # 允許空白與空行
        input_str = " 1\n\n 3\n  1 3 2  \n"
        expected = "Optimal train swapping takes 1 swaps."
        self.assertEqual(_run_solution(input_str), expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
