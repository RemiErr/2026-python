import io
import sys
import unittest
import importlib.util
from pathlib import Path

# 單元測試目標：UVA 272 (TEX Quotes)
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
        base / "QUESTION-272-su.py",
        base / "QUESTION-272-easy.py",
        base / "uva_272.py",
        base / "solution_272.py",
        base / "uva272.py",
        base / "c007.py",
    ]
    for path in candidates:
        if path.exists():
            return path

    # 其次嘗試 solutions 子目錄中含 272 / uva272 / c007 的檔案
    solutions_dir = base
    if solutions_dir.exists():
        found = []
        for path in solutions_dir.rglob("*.py"):
            name = path.name.lower()
            if name.startswith("test_"):
                continue
            if ("272" in name) or ("uva272" in name) or ("c007" in name):
                found.append(path)
        if found:
            return sorted(found)[0]

    # 如果都找不到，就回傳第一個候選，方便顯示錯誤訊息
    return candidates[0]


def _load_solution_module():
    path = _find_solution_path()
    if not path.exists():
        raise AssertionError(
            "找不到 UVA 272 的解法檔案。\n"
            "請將解法放在 weeks/week-03/ 內，或放在 weeks/week-03/solutions/<student-id>/ 下，\n"
            "檔名建議包含 272 / uva272 / c007，例如 uva_272.py。"
        )

    spec = importlib.util.spec_from_file_location("uva272_solution", path)
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


class TestUVA272(unittest.TestCase):
    """UVA 272：確認雙引號替換成 TeX 引號的結果。"""

    def test_sample_sentence(self):
        # 題目敘述中的經典句子
        input_str = '"To be or not to be," quoth the bard, "that is the question."\n'
        expected = "``To be or not to be,'' quoth the bard, ``that is the question.''\n"
        self.assertEqual(_run_solution(input_str), expected)

    def test_multiple_lines(self):
        # 多行輸入，逐行替換
        input_str = "\n".join(
            [
                '"Hello," she said.',
                '"World!"',
                "",  # 空行
                '"Bye."',
            ]
        ) + "\n"
        expected = "\n".join(
            [
                "``Hello,'' she said.",
                "``World!''",
                "",
                "``Bye.''",
            ]
        ) + "\n"
        self.assertEqual(_run_solution(input_str), expected)

    def test_no_quotes(self):
        # 沒有任何雙引號時，輸出應完全相同
        input_str = "No quotes here.\n"
        expected = "No quotes here.\n"
        self.assertEqual(_run_solution(input_str), expected)

    def test_alternating_quotes(self):
        # 連續多個引號，依序交替 `` 與 ''
        input_str = '"A" "B" "C"\n'
        expected = "``A'' ``B'' ``C''\n"
        self.assertEqual(_run_solution(input_str), expected)

    def test_quotes_across_lines(self):
        # 引號狀態需跨行延續
        input_str = '"A\nB"\n'
        expected = "``A\nB''\n"
        self.assertEqual(_run_solution(input_str), expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
