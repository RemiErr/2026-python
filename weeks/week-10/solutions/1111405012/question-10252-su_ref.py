import sys


def read_cases(text):
    numbers = list(map(int, text.split()))
    if not numbers:
        return []

    index = 0
    total_cases = numbers[index]
    index += 1
    cases = []

    for _ in range(total_cases):
        point_count = numbers[index]
        index += 1
        points = []

        for _ in range(point_count):
            x = numbers[index]
            y = numbers[index + 1]
            index += 2
            points.append((x, y))

        cases.append(points)

    return cases


def median_interval(values):
    """曼哈頓距離的最佳點會落在中位數區間。"""
    ordered = sorted(values)
    size = len(ordered)
    left = ordered[(size - 1) // 2]
    right = ordered[size // 2]
    return ordered, left, right


def total_distance(values, target):
    return sum(abs(value - target) for value in values)


def solve_one(points):
    xs = [x for x, _ in points]
    ys = [y for _, y in points]
    sorted_xs, left_x, right_x = median_interval(xs)
    sorted_ys, left_y, right_y = median_interval(ys)

    best = total_distance(sorted_xs, left_x) + total_distance(sorted_ys, left_y)
    count = (right_x - left_x + 1) * (right_y - left_y + 1)
    return f"{best} {count}"


def solve(text):
    answers = []

    for points in read_cases(text):
        answers.append(solve_one(points))

    return "\n".join(answers)


if __name__ == "__main__":
    sys.stdout.write(solve(sys.stdin.read()))
