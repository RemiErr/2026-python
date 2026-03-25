"""UVA 10041 的正式解答。"""

from __future__ import annotations

import sys


def minimum_total_distance(addresses: list[int]) -> int:
    """利用中位數找出最小總距離。"""
    sorted_addresses = sorted(addresses)
    median_address = sorted_addresses[(len(sorted_addresses) - 1) // 2]
    return sum(abs(address - median_address) for address in sorted_addresses)


def solve(data: str) -> str:
    """依照輸入格式回傳每組測資的最小總距離。"""
    tokens = [int(token) for token in data.split()]
    if not tokens:
        return ""

    case_count = tokens[0]
    index = 1
    results: list[str] = []

    for _ in range(case_count):
        relative_count = tokens[index]
        index += 1
        addresses = tokens[index:index + relative_count]
        index += relative_count
        results.append(str(minimum_total_distance(addresses)))

    return "\n".join(results)


def main() -> None:
    """提供命令列執行入口。"""
    sys.stdout.write(solve(sys.stdin.read()))


if __name__ == "__main__":
    main()
