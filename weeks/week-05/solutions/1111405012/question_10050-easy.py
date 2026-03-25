"""UVA 10050 的簡單版解答。"""

from __future__ import annotations

import sys


def count_lost_workdays(total_days: int, hartal_parameters: list[int]) -> int:
    """簡單版用布林陣列標記停工日。"""
    lost_days = [False] * (total_days + 1)

    for hartal_parameter in hartal_parameters:
        for day_number in range(hartal_parameter, total_days + 1, hartal_parameter):
            if day_number % 7 not in (6, 0):
                lost_days[day_number] = True

    return sum(lost_days)


def solve(data: str) -> str:
    """依序讀入每組測資並輸出答案。"""
    numbers = [int(token) for token in data.split()]
    if not numbers:
        return ""

    test_case_count = numbers[0]
    index = 1
    answers: list[str] = []

    for _ in range(test_case_count):
        total_days = numbers[index]
        index += 1
        party_count = numbers[index]
        index += 1
        hartals = numbers[index:index + party_count]
        index += party_count
        answers.append(str(count_lost_workdays(total_days, hartals)))

    return "\n".join(answers)


def main() -> None:
    """提供命令列執行入口。"""
    sys.stdout.write(solve(sys.stdin.read()))


if __name__ == "__main__":
    main()
