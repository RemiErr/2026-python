from __future__ import annotations

import math
import sys


def find_group_size(start_people: int, day_number: int) -> int:
    # 令 sum(start_people ... answer) >= day_number，找最小的 answer。
    target = (start_people - 1) * start_people + 2 * day_number
    answer = (math.isqrt(1 + 4 * target) - 1) // 2
    if answer < start_people:
        answer = start_people

    while answer * (answer + 1) < target:
        answer += 1

    return answer


def solve(data: str) -> str:
    tokens = data.split()
    if not tokens:
        return ""

    output: list[str] = []
    for index in range(0, len(tokens), 2):
        start_people = int(tokens[index])
        day_number = int(tokens[index + 1])
        output.append(str(find_group_size(start_people, day_number)))

    return "\n".join(output)


def main() -> None:
    sys.stdout.write(solve(sys.stdin.read()))


if __name__ == "__main__":
    main()
