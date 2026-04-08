from __future__ import annotations

import sys


class Fenwick:
    """記錄每個牛號現在還在不在。"""

    def __init__(self, n: int) -> None:
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, i: int, value: int) -> None:
        while i <= self.n:
            self.bit[i] += value
            i += i & -i

    def pick_kth(self, k: int) -> int:
        """把目前第 k 小的牛號找出來。"""
        i = 0
        step = 1 << (self.n.bit_length() - 1)

        while step:
            nxt = i + step
            if nxt <= self.n and self.bit[nxt] < k:
                k -= self.bit[nxt]
                i = nxt
            step >>= 1

        return i + 1


def solve(data: str) -> str:
    parts = data.split()
    if not parts:
        return ""

    n = int(parts[0])
    before = [0] + [int(x) for x in parts[1:1 + max(0, n - 1)]]

    tree = Fenwick(n)
    for number in range(1, n + 1):
        tree.add(number, 1)

    answer = [0] * n

    # 倒著做，因為最後一個位置剩下哪些牛號最清楚。
    for pos in range(n - 1, -1, -1):
        order = before[pos] + 1
        answer[pos] = tree.pick_kth(order)
        tree.add(answer[pos], -1)

    return "\n".join(str(x) for x in answer)


def main() -> None:
    sys.stdout.write(solve(sys.stdin.read()))


if __name__ == "__main__":
    main()
