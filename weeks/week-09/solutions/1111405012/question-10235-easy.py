import sys


MOD = 1_000_000_007


def read_row(line, width):
    parts = line.split()
    if len(parts) == width:
        return [int(x) for x in parts]
    if len(parts) == 1 and len(parts[0]) == width:
        return [int(ch) for ch in parts[0]]
    raise ValueError("invalid row")


def add_count(box, key, value):
    box[key] = (box.get(key, 0) + value) % MOD


def solve_one(board):
    rows = len(board)
    cols = len(board[0])
    dp = {(0, 0): 1}

    for r in range(rows):
        for c in range(cols):
            bit = 1 << c
            new_dp = {}

            for (mask, left), ways in dp.items():
                up = 1 if mask & bit else 0

                if board[r][c] == 0:
                    if up == 0 and left == 0:
                        add_count(new_dp, (mask & ~bit, 0), ways)
                    continue

                go_right = c + 1 < cols and board[r][c + 1] == 1
                go_down = r + 1 < rows and board[r + 1][c] == 1
                degree = up + left

                # 每個 1 格都要被同一條或不同條蛇「接到兩次」。
                if degree == 2:
                    add_count(new_dp, (mask & ~bit, 0), ways)
                elif degree == 1:
                    if go_right:
                        add_count(new_dp, (mask & ~bit, 1), ways)
                    if go_down:
                        add_count(new_dp, (mask | bit, 0), ways)
                elif degree == 0:
                    if go_right and go_down:
                        add_count(new_dp, (mask | bit, 1), ways)

            dp = new_dp

    return dp.get((0, 0), 0)


def solve(text):
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        return ""

    t = int(lines[0])
    index = 1
    ans = []

    for case_id in range(1, t + 1):
        n, m = map(int, lines[index].split())
        index += 1
        board = []

        for _ in range(n):
            board.append(read_row(lines[index], m))
            index += 1

        ans.append(f"Case {case_id}: {solve_one(board)}")

    return "\n".join(ans)


if __name__ == "__main__":
    sys.stdout.write(solve(sys.stdin.read()))
