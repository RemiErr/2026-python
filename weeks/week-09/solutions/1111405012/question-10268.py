import sys


MAX_TRIALS = 63
MAX_BALLOONS = 100


def build_table():
    reachable = [[0] * (MAX_BALLOONS + 1) for _ in range(MAX_TRIALS + 1)]

    for trial_count in range(1, MAX_TRIALS + 1):
        for balloon_count in range(1, MAX_BALLOONS + 1):
            reachable[trial_count][balloon_count] = (
                reachable[trial_count - 1][balloon_count - 1]
                + reachable[trial_count - 1][balloon_count]
                + 1
            )

    return reachable


REACHABLE = build_table()


def solve(text):
    answers = []

    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue

        balloon_count, floor_count = map(int, line.split())
        if balloon_count == 0:
            break

        answer = "More than 63 trials needed."
        for trial_count in range(1, MAX_TRIALS + 1):
            if REACHABLE[trial_count][balloon_count] >= floor_count:
                answer = str(trial_count)
                break

        answers.append(answer)

    return "\n".join(answers)


if __name__ == "__main__":
    sys.stdout.write(solve(sys.stdin.read()))
