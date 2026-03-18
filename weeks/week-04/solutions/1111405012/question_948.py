"""UVA 948 假幣判斷解法，透過每次秤重逐步縮小可疑硬幣範圍。"""

from __future__ import annotations

from typing import Optional


def _next_non_empty(lines: list[str], index: int) -> tuple[Optional[str], int]:
    """回傳下一行非空白內容，並同步更新目前讀取位置。"""
    while index < len(lines) and not lines[index].strip():
        index += 1
    if index >= len(lines):
        return None, index
    return lines[index].strip(), index + 1


def solve(data: str) -> str:
    lines = data.splitlines()
    cursor = 0

    first_line, cursor = _next_non_empty(lines, cursor)
    if first_line is None:
        return ""

    case_count = int(first_line)
    outputs: list[str] = []

    for _ in range(case_count):
        # 每組資料先讀取硬幣數量 n 與秤重次數 k。
        nk_line, cursor = _next_non_empty(lines, cursor)
        if nk_line is None:
            break

        n, k = map(int, nk_line.split())

        # possible 內容是 (硬幣編號, H/L)，H 表示可能偏重，L 表示可能偏輕。
        possible: set[tuple[int, str]] = set()
        for coin in range(1, n + 1):
            possible.add((coin, "H"))
            possible.add((coin, "L"))

        for _ in range(k):
            weigh_line, cursor = _next_non_empty(lines, cursor)
            if weigh_line is None:
                break

            numbers = list(map(int, weigh_line.split()))
            p = numbers[0]
            left = set(numbers[1 : 1 + p])
            right = set(numbers[1 + p : 1 + 2 * p])
            involved = left | right

            # 讀取本次秤重結果：= 代表平衡，< / > 代表左右盤重量關係。
            result, cursor = _next_non_empty(lines, cursor)
            if result is None:
                result = "="

            valid: set[tuple[int, str]] = set()

            if result == "=":
                # 平衡時，天平上的硬幣都不可能是假幣。
                for coin, state in possible:
                    if coin not in involved:
                        valid.add((coin, state))
            elif result == "<":
                # 左輕右重：左盤只可能是假幣偏輕；右盤只可能是假幣偏重。
                for coin, state in possible:
                    if coin in left and state == "L":
                        valid.add((coin, state))
                    elif coin in right and state == "H":
                        valid.add((coin, state))
            elif result == ">":
                # 左重右輕：左盤只可能是假幣偏重；右盤只可能是假幣偏輕。
                for coin, state in possible:
                    if coin in left and state == "H":
                        valid.add((coin, state))
                    elif coin in right and state == "L":
                        valid.add((coin, state))
            else:
                valid = set(possible)

            # 每次秤重後，只保留仍與觀察結果相符的可能性。
            possible = valid

        # 只要剩下一枚硬幣仍可能是假幣，就輸出它的編號；否則輸出 0。
        candidate_coins = {coin for coin, _ in possible}
        if len(candidate_coins) == 1:
            outputs.append(str(next(iter(candidate_coins))))
        else:
            outputs.append("0")

    return "\n\n".join(outputs)


def main() -> None:
    import sys

    result = solve(sys.stdin.read())
    if result:
        sys.stdout.write(result + "\n")


if __name__ == "__main__":
    main()
