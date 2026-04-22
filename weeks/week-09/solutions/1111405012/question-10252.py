import sys


def solve(text):
    data = list(map(int, text.split()))
    if not data:
        return ""

    index = 0
    case_count = data[index]
    index += 1
    answers = []

    for _ in range(case_count):
        point_count = data[index]
        index += 1
        xs = []
        ys = []

        for _ in range(point_count):
            xs.append(data[index])
            ys.append(data[index + 1])
            index += 2

        xs.sort()
        ys.sort()

        left_x = xs[(point_count - 1) // 2]
        right_x = xs[point_count // 2]
        left_y = ys[(point_count - 1) // 2]
        right_y = ys[point_count // 2]

        # 只要落在中位數區間內，曼哈頓距離和都會一樣小。
        best_x = left_x
        best_y = left_y
        total_distance = sum(abs(x - best_x) for x in xs) + sum(abs(y - best_y) for y in ys)
        way_count = (right_x - left_x + 1) * (right_y - left_y + 1)

        answers.append(f"{total_distance} {way_count}")

    return "\n".join(answers)


if __name__ == "__main__":
    sys.stdout.write(solve(sys.stdin.read()))
