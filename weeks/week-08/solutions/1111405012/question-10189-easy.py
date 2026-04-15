from sys import stdin, stdout


def main():
    # 先把所有輸入行讀進來，方便用索引一題一題往下走。
    lines = stdin.read().splitlines()
    i = 0
    case_no = 1
    out = []

    while i < len(lines):
        # 有些資料可能夾空白行，先跳過。
        if not lines[i].strip():
            i += 1
            continue

        n, m = map(int, lines[i].split())
        i += 1

        # 0 0 代表輸入結束。
        if n == 0 and m == 0:
            break

        board = []
        for _ in range(n):
            board.append(lines[i].strip())
            i += 1

        # 每一題前面都要先印出 Field 編號。
        out.append(f"Field #{case_no}:")

        for r in range(n):
            line = ""
            for c in range(m):
                if board[r][c] == "*":
                    line += "*"
                else:
                    count = 0

                    for dr in (-1, 0, 1):
                        for dc in (-1, 0, 1):
                            if dr == 0 and dc == 0:
                                continue

                            nr = r + dr
                            nc = c + dc

                            if 0 <= nr < n and 0 <= nc < m:
                                if board[nr][nc] == "*":
                                    count += 1

                    line += str(count)

            out.append(line)

        # 題目要求不同 Field 之間要空一行。
        out.append("")
        case_no += 1

    if out and out[-1] == "":
        out.pop()

    stdout.write("\n".join(out))


if __name__ == "__main__":
    main()
