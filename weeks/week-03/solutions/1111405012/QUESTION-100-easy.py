from __future__ import annotations

import sys

# UVA 100 - 3n+1 問題（簡易版）
# 做法：直接計算每個 n 的 cycle length，區間內取最大值
# 重點概念：
# 1. cycle length 定義為從 n 走到 1 的步數（包含起點 n 與終點 1）。
# 2. 每筆輸入給一對 i, j，要在區間 [min(i, j), max(i, j)] 找最大值。
# 3. 輸出要保留原始 i, j 的順序。


def cycle_length(n: int) -> int:
    """計算 n 的 cycle length（含 n 與 1）。"""
    # 起點本身就算一步
    length = 1
    while n != 1:
        # 奇數：3n + 1；偶數：n / 2
        if n % 2 == 1:
            n = 3 * n + 1
        else:
            n //= 2
        # 每走一步就累加
        length += 1
    return length


def solve(input_str: str) -> str:
    # 將所有數字拆成 token（以空白與換行分隔）
    tokens = input_str.split()
    if not tokens:
        return ""

    out = []
    # 兩兩讀取 (i, j)
    for i in range(0, len(tokens) - 1, 2):
        a = int(tokens[i])
        b = int(tokens[i + 1])
        # 計算區間邊界（注意輸出仍用原始 a, b）
        lo, hi = (a, b) if a <= b else (b, a)

        max_len = 0
        for n in range(lo, hi + 1):
            # 逐一計算 cycle length，取最大
            max_len = max(max_len, cycle_length(n))

        # 輸出要保留原始順序
        out.append(f"{a} {b} {max_len}")

    return "\n".join(out)


def main() -> None:
    data = sys.stdin.read()
    result = solve(data)
    if result:
        sys.stdout.write(result)


if __name__ == "__main__":
    main()
