from __future__ import annotations

import sys


def build_valid_states(width: int) -> tuple[list[int], dict[int, int]]:
    states: list[int] = []
    cannon_count: dict[int, int] = {}

    for state in range(1 << width):
        if state & (state << 1):
            continue
        if state & (state << 2):
            continue
        states.append(state)
        cannon_count[state] = state.bit_count()

    return states, cannon_count


def max_cannons(grid: list[str]) -> int:
    if not grid:
        return 0

    width = len(grid[0])
    valid_states, cannon_count = build_valid_states(width)

    allowed_states_per_row: list[list[int]] = []
    for row in grid:
        blocked = 0
        for column, terrain in enumerate(row):
            if terrain == "H":
                blocked |= 1 << column
        allowed_states_per_row.append(
            [state for state in valid_states if state & blocked == 0]
        )

    # dp[(前一列狀態, 前兩列狀態)] = 目前最多炮兵數
    current = {(0, 0): 0}

    for row_states in allowed_states_per_row:
        next_dp: dict[tuple[int, int], int] = {}
        for current_state in row_states:
            current_count = cannon_count[current_state]
            for (prev_state, prev_prev_state), best in current.items():
                if current_state & prev_state:
                    continue
                if current_state & prev_prev_state:
                    continue
                key = (current_state, prev_state)
                value = best + current_count
                saved = next_dp.get(key, -1)
                if value > saved:
                    next_dp[key] = value
        current = next_dp

    return max(current.values(), default=0)


def solve(data: str) -> str:
    lines = [line.strip() for line in data.splitlines() if line.strip()]
    if not lines:
        return ""

    row_count, _ = map(int, lines[0].split())
    grid = lines[1:1 + row_count]
    return str(max_cannons(grid))


def main() -> None:
    sys.stdout.write(solve(sys.stdin.read()))


if __name__ == "__main__":
    main()
