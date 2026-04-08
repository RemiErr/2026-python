from __future__ import annotations

from collections import Counter
import sys


def count_sextuples(numbers: list[int]) -> int:
    # 先統計所有有序的兩數和。
    pair_count: Counter[int] = Counter()
    for first in numbers:
        for second in numbers:
            pair_count[first + second] += 1

    pair_items = list(pair_count.items())

    # 再把第三個數加進去，得到所有有序三數和的數量。
    triple_count: Counter[int] = Counter()
    for third in numbers:
        for pair_sum, ways in pair_items:
            triple_count[pair_sum + third] += ways

    triple_items = list(triple_count.items())

    # 五數和可拆成三數和 + 兩數和，最後再比對 f 是否在集合裡。
    answer = 0
    for target in numbers:
        for triple_sum, triple_ways in triple_items:
            answer += triple_ways * pair_count.get(target - triple_sum, 0)

    return answer


def solve(data: str) -> str:
    tokens = data.split()
    if not tokens:
        return ""

    count = int(tokens[0])
    numbers = [int(value) for value in tokens[1:1 + count]]
    return str(count_sextuples(numbers))


def main() -> None:
    sys.stdout.write(solve(sys.stdin.read()))


if __name__ == "__main__":
    main()
