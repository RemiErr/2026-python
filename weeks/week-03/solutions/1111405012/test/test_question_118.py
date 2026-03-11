import io
import sys
import unittest
import importlib.util
from pathlib import Path

# 單元測試目標：UVA 118 (Robot)
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
        base / "QUESTION-118-su.py",
        base / "QUESTION-118-easy.py",
        base / "uva_118.py",
        base / "solution_118.py",
        base / "uva118.py",
        base / "c082.py",
    ]
    for path in candidates:
        if path.exists():
            return path

    # 其次嘗試 solutions 子目錄中含 118 / uva118 / c082 的檔案
    solutions_dir = base
    if solutions_dir.exists():
        found = []
        for path in solutions_dir.rglob("*.py"):
            name = path.name.lower()
            if name.startswith("test_"):
                continue
            if ("118" in name) or ("uva118" in name) or ("c082" in name):
                found.append(path)
        if found:
            return sorted(found)[0]

    # 如果都找不到，就回傳第一個候選，方便顯示錯誤訊息
    return candidates[0]


def _load_solution_module():
    path = _find_solution_path()
    if not path.exists():
        raise AssertionError(
            "找不到 UVA 118 的解法檔案。\n"
            "請將解法放在 weeks/week-03/ 內，或放在 weeks/week-03/solutions/<student-id>/ 下，\n"
            "檔名建議包含 118 / uva118 / c082，例如 uva_118.py。"
        )

    spec = importlib.util.spec_from_file_location("uva118_solution", path)
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


class TestUVA118(unittest.TestCase):
    """UVA 118：確認機器人最終位置與 LOST 標記是否正確。"""

    def test_official_sample(self):
        # UVA 118 標準範例
        input_str = "\n".join(
            [
                "5 3",
                "1 1 E",
                "RFRFRFRF",
                "3 2 N",
                "FRRFLLFFRRFLL",
                "0 3 W",
                "LLFFFLFLFL",
            ]
        )
        expected = "\n".join(
            [
                "1 1 E",
                "3 3 N LOST",
                "2 3 S",
            ]
        )
        self.assertEqual(_run_solution(input_str), expected)

    def test_scent_prevents_fall(self):
        # 第一台機器人掉落並留下 scent，第二台會忽略致命的 F 指令
        input_str = "\n".join(
            [
                "1 1",
                "1 1 N",
                "F",
                "1 1 N",
                "F",
            ]
        )
        expected = "\n".join(
            [
                "1 1 N LOST",
                "1 1 N",
            ]
        )
        self.assertEqual(_run_solution(input_str), expected)

    def test_rotation_only(self):
        # 只旋轉不移動
        input_str = "\n".join(
            [
                "2 2",
                "1 1 N",
                "RRRR",
            ]
        )
        expected = "1 1 N"
        self.assertEqual(_run_solution(input_str), expected)

    def test_move_within_bounds(self):
        # 在邊界內正常移動
        input_str = "\n".join(
            [
                "2 2",
                "0 0 N",
                "FFRFF",
            ]
        )
        expected = "2 2 E"
        self.assertEqual(_run_solution(input_str), expected)

    def test_whitespace_and_blank_lines(self):
        # 允許空白與空行
        input_str = " 5 3\n\n 1 1 E\nRFRFRFRF\n"
        expected = "1 1 E"
        self.assertEqual(_run_solution(input_str), expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
