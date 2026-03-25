"""UVA 10041 的簡單版解答。"""

from __future__ import annotations

import sys


def minimum_total_distance(addresses: list[int]) -> int:
    """簡單版直接排序後抓中間位置。"""
    addresses.sort()
    middle = (len(addresses) - 1) // 2
    home = addresses[middle]
    total_distance = 0

    for address in addresses:
        total_distance += abs(address - home)

    return total_distance


def solve(data: str) -> str:
    """把所有測資逐一算出答案。"""
    numbers = [int(token) for token in data.split()]
    if not numbers:
        return ""

    test_case_count = numbers[0]
    index = 1
    answers: list[str] = []

    for _ in range(test_case_count):
        count = numbers[index]
        index += 1
        family = numbers[index:index + count]
        index += count
        answers.append(str(minimum_total_distance(family)))

    return "\n".join(answers)


def main() -> None:
    """提供命令列執行入口。"""
    sys.stdout.write(solve(sys.stdin.read()))


if __name__ == "__main__":
    main()
