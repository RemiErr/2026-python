from __future__ import annotations

import sys


class FenwickTree:
    """用樹狀陣列維護目前還沒被拿走的牛號。"""

    def __init__(self, size: int) -> None:
        self.size = size
        self.tree = [0] * (size + 1)

    def add(self, index: int, value: int) -> None:
        while index <= self.size:
            self.tree[index] += value
            index += index & -index

    def find_kth(self, kth: int) -> int:
        """找出目前第 kth 小的可用牛號。"""
        index = 0
        bit = 1 << (self.size.bit_length() - 1)

        while bit:
            next_index = index + bit
            if next_index <= self.size and self.tree[next_index] < kth:
                kth -= self.tree[next_index]
                index = next_index
            bit >>= 1

        return index + 1


def restore_order(smaller_counts: list[int]) -> list[int]:
    cow_count = len(smaller_counts) + 1
    smaller_before = [0] + smaller_counts

    available = FenwickTree(cow_count)
    for cow_id in range(1, cow_count + 1):
        available.add(cow_id, 1)

    answer = [0] * cow_count

    # 從最後一個位置往前推，可以直接知道要拿第幾小的牛號。
    for position in range(cow_count - 1, -1, -1):
        kth = smaller_before[position] + 1
        answer[position] = available.find_kth(kth)
        available.add(answer[position], -1)

    return answer


def solve(data: str) -> str:
    tokens = data.split()
    if not tokens:
        return ""

    cow_count = int(tokens[0])
    smaller_counts = [int(value) for value in tokens[1:1 + max(0, cow_count - 1)]]
    answer = restore_order(smaller_counts)
    return "\n".join(str(value) for value in answer)


def main() -> None:
    sys.stdout.write(solve(sys.stdin.read()))


if __name__ == "__main__":
    main()
