"""題目 10056 的單元測試。"""

from __future__ import annotations

from test_support import DualSolutionTestCase


class TestQuestion10056(DualSolutionTestCase):
    """驗證指定玩家的獲勝機率。"""

    QUESTION_ID = "10056"

    def test_single_player_eventually_wins(self) -> None:
        self.assert_both_solutions("1\n1 0.5 1\n", "1.0000")

    def test_second_player_probability(self) -> None:
        self.assert_both_solutions("1\n3 0.5 2\n", "0.2857")

    def test_zero_success_probability(self) -> None:
        self.assert_both_solutions("1\n4 0.0 3\n", "0.0000")
