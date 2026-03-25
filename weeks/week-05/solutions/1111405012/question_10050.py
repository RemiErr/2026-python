"""UVA 10050 的正式解答。"""

from __future__ import annotations

import sys


def is_weekend(day_number: int) -> bool:
    """第 6 天是星期五，第 7 天是星期六。"""
    return day_number % 7 in {6, 0}


def count_lost_workdays(total_days: int, hartal_parameters: list[int]) -> int:
    """把所有真正停工的工作天放進集合中去重。"""
    lost_days: set[int] = set()

    for hartal_parameter in hartal_parameters:
        for day_number in range(hartal_parameter, total_days + 1, hartal_parameter):
            if not is_weekend(day_number):
                lost_days.add(day_number)

    return len(lost_days)


def solve(data: str) -> str:
    """計算每組測資損失的工作天數。"""
    tokens = [int(token) for token in data.split()]
    if not tokens:
        return ""

    case_count = tokens[0]
    index = 1
    results: list[str] = []

    for _ in range(case_count):
        total_days = tokens[index]
        index += 1
        party_count = tokens[index]
        index += 1
        hartal_parameters = tokens[index:index + party_count]
        index += party_count
        results.append(str(count_lost_workdays(total_days, hartal_parameters)))

    return "\n".join(results)


def main() -> None:
    """提供命令列執行入口。"""
    sys.stdout.write(solve(sys.stdin.read()))


if __name__ == "__main__":
    main()
