import sys


class FenwickTree:
    def __init__(self, size: int) -> None:
        self.size = size
        self.values = [0] * (size + 1)

    def update(self, index: int, delta: int) -> None:
        while index <= self.size:
            self.values[index] += delta
            index += index & -index

    def query(self, index: int) -> int:
        total = 0
        while index > 0:
            total += self.values[index]
            index -= index & -index
        return total


def solve(data: str) -> str:
    numbers = [int(token) for token in data.split()]
    if not numbers:
        return ""

    n = numbers[0]
    q = numbers[1]
    index = 2
    tree = FenwickTree(n)
    state = [0] * (n + 1)
    answers: list[str] = []

    for _ in range(q):
        operation = numbers[index]
        index += 1

        if operation == 1:
            position = numbers[index]
            index += 1

            if state[position] == 0:
                state[position] = 1
                tree.update(position, 1)
            else:
                state[position] = 0
                tree.update(position, -1)
        else:
            left = numbers[index]
            right = numbers[index + 1]
            index += 2

            decreasing_count = tree.query(right) - tree.query(left - 1)
            answers.append(str(decreasing_count % 2))

    return "\n".join(answers)


def main() -> None:
    sys.stdout.write(solve(sys.stdin.read()))


if __name__ == "__main__":
    main()
