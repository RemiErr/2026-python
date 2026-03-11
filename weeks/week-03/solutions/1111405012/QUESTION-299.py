from __future__ import annotations

import sys
from typing import List

# UVA 299 - Train Swapping
# 解題重點：計算最少相鄰交換次數，等同於序列的逆序數


def _count_swaps(nums: List[int]) -> int:
    """用氣泡排序方式計算最少交換次數（逆序數）。"""
    swaps = 0
    arr = nums[:]
    n = len(arr)
    for i in range(n):
        for j in range(n - 1 - i):
            if arr[j] > arr[j + 1]:
                # 相鄰交換一次
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swaps += 1
    return swaps


def solve(input_str: str) -> str:
    """處理輸入字串並回傳輸出字串。"""
    tokens = input_str.split()
    if not tokens:
        return ""

    t = int(tokens[0])
    idx = 1
    outputs: List[str] = []

    for _ in range(t):
        if idx >= len(tokens):
            break
        length = int(tokens[idx])
        idx += 1
        # 讀取長度為 L 的排列
        seq = list(map(int, tokens[idx : idx + length]))
        idx += length

        swaps = _count_swaps(seq)
        outputs.append(f"Optimal train swapping takes {swaps} swaps.")

    return "\n".join(outputs)


def main() -> None:
    """stdin/stdout 介面。"""
    data = sys.stdin.read()
    output = solve(data)
    if output:
        sys.stdout.write(output)


if __name__ == "__main__":
    main()
