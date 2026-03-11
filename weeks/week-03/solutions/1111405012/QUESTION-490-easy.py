from __future__ import annotations

import sys

# UVA 490 - Rotating Sentences（簡易版）
# 做法：把多行文字補空白成矩形，再順時針旋轉輸出
# 重點概念：
# 1. 先補空白把每行長度統一成矩形。
# 2. 旋轉後的第 1 行 = 原本最後一行的第 1 個字元一路往上。
# 3. 右側多餘空白要去掉（避免行尾空白）。


def solve(input_str: str) -> str:
    # 讀入所有行（保留空白）
    lines = input_str.splitlines()
    if not lines:
        return ""

    # 找最長行長度
    max_len = max(len(line) for line in lines)
    # 右側補空白，形成矩形
    padded = [line.ljust(max_len) for line in lines]

    out_lines = []
    for col in range(max_len):
        # 從最後一行往上取同一欄
        line = "".join(padded[row][col] for row in range(len(padded) - 1, -1, -1))
        # 去掉行尾多餘空白
        out_lines.append(line.rstrip())

    # UVA 490 需要輸出末尾換行
    return "\n".join(out_lines) + "\n"


def main() -> None:
    data = sys.stdin.read()
    result = solve(data)
    if result:
        sys.stdout.write(result)


if __name__ == "__main__":
    main()
