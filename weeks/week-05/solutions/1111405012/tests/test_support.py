"""測試共用工具。"""

from __future__ import annotations

from functools import lru_cache
from importlib import import_module, util
from pathlib import Path
import sys
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


@lru_cache(maxsize=None)
def load_standard_solution(question_id: str):
    """載入正式版解答模組。"""
    return import_module(f"question_{question_id}")


@lru_cache(maxsize=None)
def load_easy_solution(question_id: str):
    """從 `-easy.py` 檔案載入簡單版解答。"""
    file_path = PROJECT_ROOT / f"question_{question_id}-easy.py"
    module_name = f"question_{question_id}_easy_file"
    spec = util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"無法載入 {file_path}")

    module = util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_solution_pair(question_id: str):
    """同時載入正式版與簡單版解答。"""
    return (
        load_standard_solution(question_id),
        load_easy_solution(question_id),
    )


class DualSolutionTestCase(unittest.TestCase):
    """讓每個測試案例同時驗證兩個版本。"""

    QUESTION_ID: str | None = None

    def assert_both_solutions(self, input_data: str, expected_output: str) -> None:
        """正式版與簡單版都必須得到相同答案。"""
        if self.QUESTION_ID is None:
            raise AssertionError("QUESTION_ID 尚未設定")

        normal_module, easy_module = load_solution_pair(self.QUESTION_ID)
        self.assertEqual(normal_module.solve(input_data), expected_output)
        self.assertEqual(easy_module.solve(input_data), expected_output)
