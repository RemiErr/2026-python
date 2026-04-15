from sys import stdin, stdout


DIRECTIONS = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),           (0, 1),
    (1, -1),  (1, 0),  (1, 1),
]


def solve_field(grid):
    """把一張地雷圖轉成含數字的答案圖。"""
    rows = len(grid)
    cols = len(grid[0])
    answer = []

    for row in range(rows):
        current_row = []
        for col in range(cols):
            if grid[row][col] == "*":
                current_row.append("*")
                continue

            mine_count = 0
            for dr, dc in DIRECTIONS:
                next_row = row + dr
                next_col = col + dc
                if 0 <= next_row < rows and 0 <= next_col < cols:
                    if grid[next_row][next_col] == "*":
                        mine_count += 1

            current_row.append(str(mine_count))

        answer.append("".join(current_row))

    return answer


def solve(text):
    """依照題目格式，處理多組 Minesweeper 測資。"""
    lines = text.splitlines()
    index = 0
    field_number = 1
    outputs = []

    while index < len(lines):
        if not lines[index].strip():
            index += 1
            continue

        rows, cols = map(int, lines[index].split())
        index += 1

        if rows == 0 and cols == 0:
            break

        grid = [lines[index + offset].strip() for offset in range(rows)]
        index += rows

        outputs.append(f"Field #{field_number}:")
        outputs.extend(solve_field(grid))
        outputs.append("")
        field_number += 1

    if outputs and outputs[-1] == "":
        outputs.pop()

    return "\n".join(outputs)


def main():
    result = solve(stdin.read())
    if result:
        stdout.write(result)


if __name__ == "__main__":
    main()
