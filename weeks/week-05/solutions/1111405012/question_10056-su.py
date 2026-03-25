import sys


def winning_probability(player_count: int, success_probability: float, target_player: int) -> float:
    if success_probability == 0:
        return 0.0

    miss_probability = 1.0 - success_probability
    first_success = (miss_probability ** (target_player - 1)
                     ) * success_probability
    repeat_factor = miss_probability ** player_count

    return first_success / (1.0 - repeat_factor)


def solve(data: str) -> str:
    parts = data.split()
    if not parts:
        return ""

    test_case_count = int(parts[0])
    index = 1
    answers: list[str] = []

    for _ in range(test_case_count):
        n = int(parts[index])
        p = float(parts[index + 1])
        i = int(parts[index + 2])
        index += 3

        answers.append(f"{winning_probability(n, p, i):.4f}")

    return "\n".join(answers)


def main() -> None:
    sys.stdout.write(solve(sys.stdin.read()))


if __name__ == "__main__":
    main()
