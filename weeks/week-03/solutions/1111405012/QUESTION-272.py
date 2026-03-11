from __future__ import annotations

import sys

# UVA 272 - TEX Quotes
# 解題重點：遇到第一個 " 轉成 ``，下一個轉成 ''，依序交替


def solve(input_str: str) -> str:
    """處理輸入字串並回傳輸出字串。"""
    out_chars = []
    # True 代表下一個雙引號要輸出 ``，False 代表輸出 ''
    open_quote = True

    for ch in input_str:
        if ch == '"':
            if open_quote:
                out_chars.append("``")
            else:
                out_chars.append("''")
            open_quote = not open_quote
        else:
            # 其他字元保持不變
            out_chars.append(ch)

    return "".join(out_chars)


def main() -> None:
    """stdin/stdout 介面。"""
    data = sys.stdin.read()
    output = solve(data)
    if output:
        sys.stdout.write(output)


if __name__ == "__main__":
    main()
