from __future__ import annotations

import sys
from typing import Dict, List, Tuple

# UVA 100 - The 3n + 1 Problem
# 解題重點：計算區間內每個 n 的 cycle length，取最大值
# 使用記憶化（memoization）降低重複計算


def _cycle_length(n: int, memo: Dict[int, int]) -> int:
    """計算 n 的 cycle length（含 n 與 1），並使用 memo 快取。"""
    if n in memo:
        return memo[n]

    seq: List[int] = []
    cur = n
    while cur not in memo:
        seq.append(cur)
        # Collatz 規則：奇數 3n+1、偶數 n/2
        if cur % 2 == 1:
            cur = 3 * cur + 1
        else:
            cur //= 2

    # cur 已有已知長度，反向回填
    length = memo[cur]
    for value in reversed(seq):
        length += 1
        # 逐步把中間結果存入快取，避免重算
        memo[value] = length

    return memo[n]


def solve(input_str: str) -> str:
    """處理輸入字串並回傳輸出字串。"""
    tokens = input_str.split()
    if not tokens:
        return ""

    # 初始化 memo，1 的 cycle length 為 1
    memo: Dict[int, int] = {1: 1}

    results: List[str] = []
    # 以兩個一組讀取 i, j
    for idx in range(0, len(tokens) - 1, 2):
        i = int(tokens[idx])
        j = int(tokens[idx + 1])
        # 區間要用排序後的邊界，但輸出要保留原始 i, j
        lo, hi = (i, j) if i <= j else (j, i)

        max_len = 0
        for n in range(lo, hi + 1):
            length = _cycle_length(n, memo)
            if length > max_len:
                max_len = length

        results.append(f"{i} {j} {max_len}")

    return "\n".join(results)


def main() -> None:
    """stdin/stdout 介面。"""
    data = sys.stdin.read()
    output = solve(data)
    if output:
        sys.stdout.write(output)


if __name__ == "__main__":
    main()
