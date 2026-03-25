"""UVA 10056 的正式解答。"""

from __future__ import annotations

import sys


def winning_probability(player_count: int, success_probability: float, target_player: int) -> float:
    """套用等比級數公式計算第 i 位玩家的獲勝機率。"""
    if success_probability == 0:
        return 0.0

    failure_probability = 1 - success_probability
    target_round_probability = (failure_probability ** (target_player - 1)) * success_probability
    full_round_failure = failure_probability ** player_count
    return target_round_probability / (1 - full_round_failure)


def solve(data: str) -> str:
    """輸出每組測資指定玩家的獲勝機率。"""
    tokens = data.split()
    if not tokens:
        return ""

    case_count = int(tokens[0])
    index = 1
    results: list[str] = []

    for _ in range(case_count):
        player_count = int(tokens[index])
        success_probability = float(tokens[index + 1])
        target_player = int(tokens[index + 2])
        index += 3
        probability = winning_probability(player_count, success_probability, target_player)
        results.append(f"{probability:.4f}")

    return "\n".join(results)


def main() -> None:
    """提供命令列執行入口。"""
    sys.stdout.write(solve(sys.stdin.read()))


if __name__ == "__main__":
    main()
