import sys


def minimum_total_distance(addresses: list[int]) -> int:
    addresses.sort()
    middle = (len(addresses) - 1) // 2
    home = addresses[middle]
    total_distance = 0

    for address in addresses:
        total_distance += abs(address - home)

    return total_distance


def solve(data: str) -> str:
    numbers = [int(token) for token in data.split()]
    if not numbers:
        return ""

    test_case_count = numbers[0]
    index = 1
    answers: list[str] = []

    for _ in range(test_case_count):
        count = numbers[index]
        index += 1
        family = numbers[index:index + count]
        index += count
        answers.append(str(minimum_total_distance(family)))

    return "\n".join(answers)


def main() -> None:
    sys.stdout.write(solve(sys.stdin.read()))


if __name__ == "__main__":
    main()
