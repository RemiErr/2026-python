from __future__ import annotations

from collections import Counter
import sys


def solve(data: str) -> str:
    parts = data.split()
    if not parts:
        return ""
    n = int(parts[0])
    nums = [int(x) for x in parts[1:1 + n]]
    two_sum: Counter[int] = Counter()
    for a in nums:
        for b in nums:
            two_sum[a + b] += 1
    two_sum_items = list(two_sum.items())
    three_sum: Counter[int] = Counter()
    for c in nums:
        for ab, ways in two_sum_items:
            three_sum[ab + c] += ways
    answer = 0
    for f in nums:
        for abc, ways in three_sum.items():
            answer += ways * two_sum.get(f - abc, 0)
    return str(answer)


def main() -> None:
    sys.stdout.write(solve(sys.stdin.read()))


if __name__ == "__main__":
    main()
