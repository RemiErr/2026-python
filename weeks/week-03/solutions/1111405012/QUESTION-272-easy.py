from __future__ import annotations

import sys

# UVA 272 - TEX Quotes（簡易版）
# 做法：遇到 " 就交替輸出 `` 和 ''
# 重點概念：
# 1. 第一個 " 轉成 ``（左雙引號）
# 2. 第二個 " 轉成 ''（右雙引號）
# 3. 之後持續交替即可


def solve(input_str: str) -> str:
    out = []
    # True 表示下一個引號要輸出 ``，False 表示要輸出 ''
    is_open = True

    for ch in input_str:
        if ch == '"':
            # 依據當前狀態輸出正確的 TeX 引號
            out.append("``" if is_open else "''")
            is_open = not is_open
        else:
            # 非引號字元直接保留
            out.append(ch)

    return "".join(out)


def main() -> None:
    data = sys.stdin.read()
    result = solve(data)
    if result:
        sys.stdout.write(result)


if __name__ == "__main__":
    main()
