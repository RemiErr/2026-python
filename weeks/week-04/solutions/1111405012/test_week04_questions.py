"""Week-04 題組整合單元測試。"""

from __future__ import annotations

import os
import sys
import unittest


# 讓測試可以直接匯入同資料夾內的題目模組。
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

import question_948
import question_10008
import question_10019
import question_10035
import question_10038


class TestQuestion948(unittest.TestCase):
    def test_can_find_unique_fake_coin_with_equal_weighing(self) -> None:
        # 驗證：當第一次平衡可排除真幣，第二次就能唯一鎖定假幣。
        input_data = """1

4 2
1 1 2
=
1 3 1
<
"""
        self.assertEqual(question_948.solve(input_data), "3")

    def test_ambiguous_case_returns_zero(self) -> None:
        # 驗證：若結果無法唯一判斷假幣，必須輸出 0。
        input_data = """2

3 1
1 1 2
=

4 1
1 1 2
<
"""
        self.assertEqual(question_948.solve(input_data), "3\n\n0")


class TestQuestion10008(unittest.TestCase):
    def test_sort_by_frequency_then_alphabet(self) -> None:
        # 驗證：相同次數時必須依字母順序輸出。
        input_data = """3
ab
BA
c
"""
        expected = """A 2
B 2
C 1"""
        self.assertEqual(question_10008.solve(input_data), expected)

    def test_case_insensitive_counting(self) -> None:
        # 驗證：大小寫要合併統計。
        input_data = """2
aA
bBbb
"""
        expected = """B 4
A 2"""
        self.assertEqual(question_10008.solve(input_data), expected)


class TestQuestion10019(unittest.TestCase):
    def test_absolute_difference_each_line(self) -> None:
        # 驗證：每行都輸出兩數絕對差，並支援 64 位元範圍大數值。
        input_data = """10 12
10 10
1 9223372036854775807
"""
        expected = """2
0
9223372036854775806"""
        self.assertEqual(question_10019.solve(input_data), expected)


class TestQuestion10035(unittest.TestCase):
    def test_primary_arithmetic_sample_style(self) -> None:
        # 驗證：0 次、1 次、多次 carry 的輸出句型要正確。
        input_data = """123 456
555 555
123 594
0 0
"""
        expected = """No carry operation.
3 carry operations.
1 carry operation."""
        self.assertEqual(question_10035.solve(input_data), expected)

    def test_cascading_carries(self) -> None:
        # 驗證：連續進位（例如 999999999 + 1）要正確計算。
        input_data = """999999999 1
0 0
"""
        expected = "9 carry operations."
        self.assertEqual(question_10035.solve(input_data), expected)


class TestQuestion10038(unittest.TestCase):
    def test_jolly_and_not_jolly_cases(self) -> None:
        # 驗證：同時涵蓋 jolly 與 not jolly 的典型輸入。
        input_data = """4 1 4 2 3
5 1 4 2 -1 6
"""
        expected = """Jolly
Not jolly"""
        self.assertEqual(question_10038.solve(input_data), expected)

    def test_single_value_sequence_is_jolly(self) -> None:
        # 驗證：長度為 1 的序列依定義一定是 Jolly。
        self.assertEqual(question_10038.solve("1 10\n"), "Jolly")


if __name__ == "__main__":
    unittest.main(verbosity=2)
