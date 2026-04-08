from __future__ import annotations

import sys


def solve(data: str) -> str:
    lines = [line.strip() for line in data.splitlines() if line.strip()]
    if not lines:
        return ""
    n, m = map(int, lines[0].split())
    board = lines[1:1 + n]
    ok_states: list[int] = []
    count_in_state: dict[int, int] = {}
    for state in range(1 << m):
        if state & (state << 1):
            continue
        if state & (state << 2):
            continue
        ok_states.append(state)
        count_in_state[state] = state.bit_count()
    row_choices: list[list[int]] = []
    for row in board:
        blocked = 0
        for col, ch in enumerate(row):
            if ch == "H":
                blocked |= 1 << col
        row_choices.append([state for state in ok_states if state & blocked == 0])
    best = {(0, 0): 0}
    for choices in row_choices:
        new_best: dict[tuple[int, int], int] = {}
        for now in choices:
            soldiers = count_in_state[now]
            for (prev1, prev2), total in best.items():
                if now & prev1:
                    continue
                if now & prev2:
                    continue
                key = (now, prev1)
                value = total + soldiers
                if value > new_best.get(key, -1):
                    new_best[key] = value
        best = new_best
    return str(max(best.values(), default=0))


def main() -> None:
    sys.stdout.write(solve(sys.stdin.read()))


if __name__ == "__main__":
    main()
