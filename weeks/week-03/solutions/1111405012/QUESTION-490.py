from __future__ import annotations

import sys
from typing import List

# UVA 490 - Rotating Sentences
# 解題重點：把多行文字視為矩陣，順時針旋轉 90 度後輸出


def solve(input_str: str) -> str:
    """處理輸入字串並回傳輸出字串。"""
    lines = input_str.splitlines()
    if not lines:
        return ""

    max_len = max(len(line) for line in lines)
    # 右邊補空白形成矩形
    padded = [line.ljust(max_len) for line in lines]

    # 由最後一行到第一行，逐欄輸出
    out_lines: List[str] = []
    for col in range(max_len):
        # 取出同一欄的字元，從最後一列往上
        chars = [padded[row][col] for row in range(len(padded) - 1, -1, -1)]
        # 右側多餘空白不輸出
        out_lines.append("".join(chars).rstrip())

    return "\n".join(out_lines) + "\n"


def main() -> None:
    """stdin/stdout 介面。"""
    data = sys.stdin.read()
    output = solve(data)
    if output:
        sys.stdout.write(output)


if __name__ == "__main__":
    main()
