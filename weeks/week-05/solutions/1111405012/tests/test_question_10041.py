"""題目 10041 的單元測試。"""

from __future__ import annotations

from test_support import DualSolutionTestCase


class TestQuestion10041(DualSolutionTestCase):
    """驗證最短總距離的計算結果。"""

    QUESTION_ID = "10041"

    def test_single_house(self) -> None:
        self.assert_both_solutions("1\n1 25\n", "0")

    def test_even_count_relatives(self) -> None:
        self.assert_both_solutions("1\n4 1 2 10 20\n", "27")

    def test_duplicate_addresses(self) -> None:
        self.assert_both_solutions("1\n5 10 10 20 30 30\n", "40")
