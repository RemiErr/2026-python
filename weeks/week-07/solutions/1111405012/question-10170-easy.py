from __future__ import annotations

import math
import sys


def people_on_day(s: int, d: int) -> int:
    # 找最小的 n，讓 s + (s+1) + ... + n 的總天數至少到第 d 天。
    target = (s - 1) * s + 2 * d
    n = (math.isqrt(1 + 4 * target) - 1) // 2
    if n < s:
        n = s
    while n * (n + 1) < target:
        n += 1
    return n


def solve(data: str) -> str:
    parts = data.split()
    if not parts:
        return ""

    answer: list[str] = []
    for i in range(0, len(parts), 2):
        s = int(parts[i])
        d = int(parts[i + 1])
        answer.append(str(people_on_day(s, d)))

    return "\n".join(answer)


def main() -> None:
    sys.stdout.write(solve(sys.stdin.read()))


if __name__ == "__main__":
    main()
