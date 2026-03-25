"""題目 10057 的單元測試。"""

from __future__ import annotations

from test_support import DualSolutionTestCase


class TestQuestion10057(DualSolutionTestCase):
    """驗證密碼候選值的統計結果。"""

    QUESTION_ID = "10057"

    def test_odd_count(self) -> None:
        self.assert_both_solutions("3\n1\n2\n3\n", "2 1 1")

    def test_even_count_with_two_best_values(self) -> None:
        self.assert_both_solutions("4\n1\n2\n3\n4\n", "2 2 2")

    def test_even_count_with_repeated_median(self) -> None:
        self.assert_both_solutions("6\n1\n2\n2\n2\n3\n4\n", "2 3 1")
