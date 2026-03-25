"""UVA 10057 的正式解答。"""

from __future__ import annotations

from bisect import bisect_left, bisect_right
import sys


def summarize_password_candidates(numbers: list[int]) -> tuple[int, int, int]:
    """回傳最小最佳值、落在最佳區間內的數量與最佳值個數。"""
    sorted_numbers = sorted(numbers)
    lower_median = sorted_numbers[(len(sorted_numbers) - 1) // 2]
    upper_median = sorted_numbers[len(sorted_numbers) // 2]

    left_index = bisect_left(sorted_numbers, lower_median)
    right_index = bisect_right(sorted_numbers, upper_median)
    count_in_best_range = right_index - left_index
    candidate_count = upper_median - lower_median + 1

    return lower_median, count_in_best_range, candidate_count


def solve(data: str) -> str:
    """題目會一直給資料到 EOF。"""
    tokens = [int(token) for token in data.split()]
    if not tokens:
        return ""

    index = 0
    results: list[str] = []

    while index < len(tokens):
        number_count = tokens[index]
        index += 1
        numbers = tokens[index:index + number_count]
        index += number_count
        best_value, count_in_best_range, candidate_count = summarize_password_candidates(numbers)
        results.append(f"{best_value} {count_in_best_range} {candidate_count}")

    return "\n".join(results)


def main() -> None:
    """提供命令列執行入口。"""
    sys.stdout.write(solve(sys.stdin.read()))


if __name__ == "__main__":
    main()
