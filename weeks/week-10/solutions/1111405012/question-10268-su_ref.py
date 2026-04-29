import sys


LIMIT = 63


def min_trials(egg_count, floor_count):
    """
    cover[e] 代表在目前 moves 次嘗試下，拿 e 顆球最多能確定多少層樓。
    轉移式：
    - 球破：少一顆球、少一次機會
    - 球沒破：球數不變、少一次機會
    - 再加上當前這一層
    """
    cover = [0] * (egg_count + 1)

    for moves in range(1, LIMIT + 1):
        for eggs in range(egg_count, 0, -1):
            cover[eggs] = cover[eggs] + cover[eggs - 1] + 1

        if cover[egg_count] >= floor_count:
            return str(moves)

    return "More than 63 trials needed."


def solve(text):
    answers = []

    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue

        egg_count, floor_count = map(int, line.split())
        if egg_count == 0:
            break

        answers.append(min_trials(egg_count, floor_count))

    return "\n".join(answers)


if __name__ == "__main__":
    sys.stdout.write(solve(sys.stdin.read()))
