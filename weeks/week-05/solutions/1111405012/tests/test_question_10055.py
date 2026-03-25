"""題目 10055 的單元測試。"""

from __future__ import annotations

from test_support import DualSolutionTestCase


class TestQuestion10055(DualSolutionTestCase):
    """驗證函數增減性的查詢結果。"""

    QUESTION_ID = "10055"

    def test_basic_toggle_and_query(self) -> None:
        input_data = "\n".join(
            [
                "5 5",
                "2 1 5",
                "1 3",
                "2 1 5",
                "1 5",
                "2 3 5",
            ]
        )
        self.assert_both_solutions(input_data + "\n", "0\n1\n0")

    def test_single_index_range(self) -> None:
        input_data = "\n".join(
            [
                "1 3",
                "2 1 1",
                "1 1",
                "2 1 1",
            ]
        )
        self.assert_both_solutions(input_data + "\n", "0\n1")

    def test_repeat_flip_changes_parity(self) -> None:
        input_data = "\n".join(
            [
                "4 7",
                "1 2",
                "2 2 2",
                "1 2",
                "1 1",
                "1 4",
                "2 1 4",
                "2 1 3",
            ]
        )
        self.assert_both_solutions(input_data + "\n", "1\n0\n1")
