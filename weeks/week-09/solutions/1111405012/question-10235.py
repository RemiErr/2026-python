import sys


MOD = 1_000_000_007


def parse_row(line, width):
    parts = line.split()
    if len(parts) == width:
        return [int(value) for value in parts]
    if len(parts) == 1 and len(parts[0]) == width:
        return [int(ch) for ch in parts[0]]
    raise ValueError("invalid row format")


def add_state(container, key, value):
    container[key] = (container.get(key, 0) + value) % MOD


def count_cycle_covers(board):
    row_count = len(board)
    column_count = len(board[0])
    states = {(0, 0): 1}

    for row_index in range(row_count):
        for column_index in range(column_count):
            bit = 1 << column_index
            next_states = {}

            for (mask, left_edge), ways in states.items():
                up_edge = 1 if mask & bit else 0
                cell_open = board[row_index][column_index] == 1

                if not cell_open:
                    if up_edge == 0 and left_edge == 0:
                        add_state(next_states, (mask & ~bit, 0), ways)
                    continue

                right_open = column_index + 1 < column_count and board[row_index][column_index + 1] == 1
                down_open = row_index + 1 < row_count and board[row_index + 1][column_index] == 1
                current_degree = up_edge + left_edge

                # 可走的格子最後一定要連到兩條邊，這裡只補上缺少的部分。
                if current_degree == 2:
                    add_state(next_states, (mask & ~bit, 0), ways)
                elif current_degree == 1:
                    if right_open:
                        add_state(next_states, (mask & ~bit, 1), ways)
                    if down_open:
                        add_state(next_states, (mask | bit, 0), ways)
                elif current_degree == 0:
                    if right_open and down_open:
                        add_state(next_states, (mask | bit, 1), ways)

            states = next_states

    return states.get((0, 0), 0)


def solve(text):
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        return ""

    case_count = int(lines[0])
    line_index = 1
    answers = []

    for case_index in range(1, case_count + 1):
        row_count, column_count = map(int, lines[line_index].split())
        line_index += 1

        board = []
        for _ in range(row_count):
            board.append(parse_row(lines[line_index], column_count))
            line_index += 1

        answers.append(f"Case {case_index}: {count_cycle_covers(board)}")

    return "\n".join(answers)


if __name__ == "__main__":
    sys.stdout.write(solve(sys.stdin.read()))
