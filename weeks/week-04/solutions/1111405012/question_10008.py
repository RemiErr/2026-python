"""UVA 10008 Cryptanalysis 解法，統計每個英文字母的出現次數。"""

from __future__ import annotations

from collections import Counter


def solve(data: str) -> str:
    lines = data.splitlines()
    if not lines:
        return ""

    # 第一行代表接下來要處理的文字行數。
    n = int(lines[0].strip() or "0")
    counter: Counter[str] = Counter()

    for line in lines[1 : 1 + n]:
        # 只統計英文字母，並統一轉成大寫後累加。
        for ch in line:
            if ch.isalpha():
                counter[ch.upper()] += 1

    # 先依出現次數由大到小排序，再依字母順序排序。
    ordered = sorted(counter.items(), key=lambda item: (-item[1], item[0]))
    return "\n".join(f"{letter} {count}" for letter, count in ordered)


def main() -> None:
    import sys

    result = solve(sys.stdin.read())
    if result:
        sys.stdout.write(result + "\n")


if __name__ == "__main__":
    main()
