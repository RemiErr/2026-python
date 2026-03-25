"""UVA 10057 的簡單版解答。"""

from __future__ import annotations

import sys


def summarize_password_candidates(numbers: list[int]) -> tuple[int, int, int]:
    """直接用排序後的中間兩個值來判斷答案。"""
    numbers.sort()
    lower = numbers[(len(numbers) - 1) // 2]
    upper = numbers[len(numbers) // 2]

    count = 0
    for value in numbers:
        if lower <= value <= upper:
            count += 1

    ways = upper - lower + 1
    return lower, count, ways


def solve(data: str) -> str:
    """一路讀到輸入結束。"""
    numbers = [int(token) for token in data.split()]
    if not numbers:
        return ""

    index = 0
    answers: list[str] = []

    while index < len(numbers):
        count = numbers[index]
        index += 1
        values = numbers[index:index + count]
        index += count
        a, matches, ways = summarize_password_candidates(values)
        answers.append(f"{a} {matches} {ways}")

    return "\n".join(answers)


def main() -> None:
    """提供命令列執行入口。"""
    sys.stdout.write(solve(sys.stdin.read()))


if __name__ == "__main__":
    main()
