"""UVA 10056 的簡單版解答。"""

from __future__ import annotations

import sys


def winning_probability(player_count: int, success_probability: float, target_player: int) -> float:
    """先算玩家第一次有機會獲勝的機率，再除以循環失敗率。"""
    if success_probability == 0:
        return 0.0

    miss_probability = 1.0 - success_probability
    first_success = (miss_probability ** (target_player - 1)) * success_probability
    repeat_factor = miss_probability ** player_count
    return first_success / (1.0 - repeat_factor)


def solve(data: str) -> str:
    """依序處理每一行輸入。"""
    parts = data.split()
    if not parts:
        return ""

    test_case_count = int(parts[0])
    index = 1
    answers: list[str] = []

    for _ in range(test_case_count):
        n = int(parts[index])
        p = float(parts[index + 1])
        i = int(parts[index + 2])
        index += 3
        answers.append(f"{winning_probability(n, p, i):.4f}")

    return "\n".join(answers)


def main() -> None:
    """提供命令列執行入口。"""
    sys.stdout.write(solve(sys.stdin.read()))


if __name__ == "__main__":
    main()
