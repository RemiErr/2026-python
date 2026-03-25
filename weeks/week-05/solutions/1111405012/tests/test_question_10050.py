"""題目 10050 的單元測試。"""

from __future__ import annotations

from test_support import DualSolutionTestCase


class TestQuestion10050(DualSolutionTestCase):
    """驗證罷會造成的工作天損失。"""

    QUESTION_ID = "10050"

    def test_sample_case(self) -> None:
        self.assert_both_solutions("1\n14\n3\n3\n4\n8\n", "5")

    def test_skip_weekends(self) -> None:
        self.assert_both_solutions("1\n7\n1\n2\n", "2")

    def test_merge_overlapping_parties(self) -> None:
        self.assert_both_solutions("1\n15\n2\n3\n5\n", "6")
