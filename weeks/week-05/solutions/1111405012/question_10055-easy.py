"""題目 10055 的簡單版解答。"""

from __future__ import annotations

import sys


class FenwickTree:
    """簡單版仍保留樹狀陣列，才能通過大資料。"""

    def __init__(self, size: int) -> None:
        self.size = size
        self.values = [0] * (size + 1)

    def update(self, index: int, delta: int) -> None:
        while index <= self.size:
            self.values[index] += delta
            index += index & -index

    def query(self, index: int) -> int:
        total = 0
        while index > 0:
            total += self.values[index]
            index -= index & -index
        return total


def solve(data: str) -> str:
    """遞減次數是奇數就輸出 1，偶數就輸出 0。"""
    numbers = [int(token) for token in data.split()]
    if not numbers:
        return ""

    n = numbers[0]
    q = numbers[1]
    index = 2
    tree = FenwickTree(n)
    state = [0] * (n + 1)
    answers: list[str] = []

    for _ in range(q):
        operation = numbers[index]
        index += 1

        if operation == 1:
            position = numbers[index]
            index += 1
            if state[position] == 0:
                state[position] = 1
                tree.update(position, 1)
            else:
                state[position] = 0
                tree.update(position, -1)
        else:
            left = numbers[index]
            right = numbers[index + 1]
            index += 2
            decreasing_count = tree.query(right) - tree.query(left - 1)
            answers.append(str(decreasing_count % 2))

    return "\n".join(answers)


def main() -> None:
    """提供命令列執行入口。"""
    sys.stdout.write(solve(sys.stdin.read()))


if __name__ == "__main__":
    main()
