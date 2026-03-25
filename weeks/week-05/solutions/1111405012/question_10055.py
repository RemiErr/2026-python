"""題目 10055 的正式解答。"""

from __future__ import annotations

import sys


class FenwickTree:
    """用來維護區間內有幾個遞減函數。"""

    def __init__(self, size: int) -> None:
        self.size = size
        self.tree = [0] * (size + 1)

    def add(self, index: int, delta: int) -> None:
        while index <= self.size:
            self.tree[index] += delta
            index += index & -index

    def prefix_sum(self, index: int) -> int:
        total = 0
        while index > 0:
            total += self.tree[index]
            index -= index & -index
        return total

    def range_sum(self, left: int, right: int) -> int:
        return self.prefix_sum(right) - self.prefix_sum(left - 1)


def solve(data: str) -> str:
    """奇數個遞減函數相乘會得到遞減函數。"""
    tokens = [int(token) for token in data.split()]
    if not tokens:
        return ""

    function_count = tokens[0]
    query_count = tokens[1]
    index = 2

    tracker = FenwickTree(function_count)
    is_decreasing = [0] * (function_count + 1)
    results: list[str] = []

    for _ in range(query_count):
        operation = tokens[index]
        index += 1

        if operation == 1:
            function_index = tokens[index]
            index += 1
            delta = 1 if is_decreasing[function_index] == 0 else -1
            is_decreasing[function_index] ^= 1
            tracker.add(function_index, delta)
            continue

        left = tokens[index]
        right = tokens[index + 1]
        index += 2
        parity = tracker.range_sum(left, right) % 2
        results.append(str(parity))

    return "\n".join(results)


def main() -> None:
    """提供命令列執行入口。"""
    sys.stdout.write(solve(sys.stdin.read()))


if __name__ == "__main__":
    main()
