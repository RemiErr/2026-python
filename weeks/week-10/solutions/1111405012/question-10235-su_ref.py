import sys
from functools import lru_cache


MOD = 1_000_000_007


def read_row(line, width):
    """題目有兩種常見格式：空白分隔或直接連在一起。"""
    parts = line.split()
    if len(parts) == width:
        return tuple(int(value) for value in parts)
    if len(parts) == 1 and len(parts[0]) == width:
        return tuple(int(ch) for ch in parts[0])
    raise ValueError("invalid row")


def count_layouts(board):
    """用記憶化搜尋計算所有合法鋪法。"""
    rows = len(board)
    cols = len(board[0])

    @lru_cache(maxsize=None)
    def dfs(pos, mask, left_open):
        # 所有格子都處理完時，不能留下往下或往右未接好的蛇身。
        if pos == rows * cols:
            return 1 if mask == 0 and left_open == 0 else 0

        r, c = divmod(pos, cols)
        bit = 1 << c
        up_open = 1 if mask & bit else 0

        if board[r][c] == 0:
            # 插座格不能被蛇佔據，所以這格上下左右都不能接進來。
            if up_open or left_open:
                return 0
            return dfs(pos + 1, mask & ~bit, 0)

        can_go_right = c + 1 < cols and board[r][c + 1] == 1
        can_go_down = r + 1 < rows and board[r + 1][c] == 1
        degree = up_open + left_open
        total = 0

        if degree == 2:
            # 已經有兩個方向接進來，這格剛好補成環上的一段。
            total = dfs(pos + 1, mask & ~bit, 0)
        elif degree == 1:
            # 只接進來一條，就必須再接出去一條。
            if can_go_right:
                total += dfs(pos + 1, mask & ~bit, 1)
            if can_go_down:
                total += dfs(pos + 1, mask | bit, 0)
        else:
            # 完全沒有接進來時，只能從這格新開一個轉角往右和往下延伸。
            if can_go_right and can_go_down:
                total = dfs(pos + 1, mask | bit, 1)

        return total % MOD

    return dfs(0, 0, 0)


def solve(text):
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        return ""

    total_cases = int(lines[0])
    index = 1
    answers = []

    for case_id in range(1, total_cases + 1):
        rows, cols = map(int, lines[index].split())
        index += 1
        board = []

        for _ in range(rows):
            board.append(read_row(lines[index], cols))
            index += 1

        answers.append(f"Case {case_id}: {count_layouts(tuple(board))}")

    return "\n".join(answers)


if __name__ == "__main__":
    sys.stdout.write(solve(sys.stdin.read()))
