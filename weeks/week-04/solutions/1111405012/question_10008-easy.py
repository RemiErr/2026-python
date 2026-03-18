"""UVA 10008 簡單版：統計每個英文字母出現的次數。"""

from __future__ import annotations


def solve(data: str) -> str:
    lines = data.splitlines()
    if not lines:
        return ""

    # 第 1 行代表後面有幾行文字需要分析。
    n = int(lines[0].strip() or "0")

    # 這裡用最基本的字典來累加次數。
    # 好處是寫法直覺，手打時也不容易忘記。
    count: dict[str, int] = {}

    # 題目只要求處理接下來 n 行文字，多的內容就忽略。
    for i in range(1, min(n + 1, len(lines))):
        # 先全部轉成大寫，之後就不用分開處理大小寫。
        line = lines[i].upper()

        for ch in line:
            # 只統計 A 到 Z，空白、數字、標點都跳過。
            if "A" <= ch <= "Z":
                count[ch] = count.get(ch, 0) + 1

    # 先轉成清單再排序，比較符合題目要求，也容易記：
    # 1. 次數多的排前面
    # 2. 次數相同時，字母小的排前面
    items = list(count.items())
    items.sort(key=lambda item: (-item[1], item[0]))

    answer_lines: list[str] = []
    for letter, times in items:
        answer_lines.append(f"{letter} {times}")

    return "\n".join(answer_lines)


def main() -> None:
    import sys

    result = solve(sys.stdin.read())
    if result:
        sys.stdout.write(result + "\n")


if __name__ == "__main__":
    main()
