from __future__ import annotations

import sys

# UVA 299 - Train Swapping（簡易版）
# 做法：使用氣泡排序計算相鄰交換次數
# 重點概念：
# 1. 最少交換次數 = 序列的逆序數。
# 2. 氣泡排序每次相鄰交換，剛好可以累計逆序數。


def solve(input_str: str) -> str:
    # 以空白拆成 token，方便讀取
    tokens = input_str.split()
    if not tokens:
        return ""

    # 第一個數字是測資數量
    t = int(tokens[0])
    idx = 1
    out = []

    for _ in range(t):
        # 讀取車廂數量 L
        l = int(tokens[idx])
        idx += 1
        # 讀取該列車的排列
        arr = list(map(int, tokens[idx : idx + l]))
        idx += l

        swaps = 0
        # 氣泡排序：每交換一次相鄰車廂就加一
        for i in range(l):
            for j in range(l - 1 - i):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    swaps += 1

        out.append(f"Optimal train swapping takes {swaps} swaps.")

    return "\n".join(out)


def main() -> None:
    data = sys.stdin.read()
    result = solve(data)
    if result:
        sys.stdout.write(result)


if __name__ == "__main__":
    main()
