def solve(data: str) -> str:
    lines: list[str] = []
    for line in data.splitlines():
        line = line.strip()
        if line:
            lines.append(line)

    if not lines:
        return ""

    index = 0
    case_count = int(lines[index])
    index += 1

    answers: list[str] = []

    for _ in range(case_count):
        n, k = map(int, lines[index].split())
        index += 1

        heavy = [True] * (n + 1)
        light = [True] * (n + 1)

        for _ in range(k):
            numbers = list(map(int, lines[index].split()))
            index += 1

            result = lines[index]
            index += 1

            p = numbers[0]
            left = numbers[1: 1 + p]
            right = numbers[1 + p: 1 + 2 * p]

            next_heavy = [False] * (n + 1)
            next_light = [False] * (n + 1)

            if result == "=":
                left_set = set(left)
                right_set = set(right)

                for coin in range(1, n + 1):
                    if coin not in left_set and coin not in right_set:
                        next_heavy[coin] = heavy[coin]
                        next_light[coin] = light[coin]

            elif result == "<":
                for coin in left:
                    if light[coin]:
                        next_light[coin] = True

                for coin in right:
                    if heavy[coin]:
                        next_heavy[coin] = True

            else:
                for coin in left:
                    if heavy[coin]:
                        next_heavy[coin] = True

                for coin in right:
                    if light[coin]:
                        next_light[coin] = True

            heavy = next_heavy
            light = next_light
        suspect_coins: list[int] = []
        for coin in range(1, n + 1):
            if heavy[coin] or light[coin]:
                suspect_coins.append(coin)

        if len(suspect_coins) == 1:
            answers.append(str(suspect_coins[0]))
        else:
            answers.append("0")
    return "\n\n".join(answers)


def main() -> None:
    import sys
    result = solve(sys.stdin.read())
    if result:
        sys.stdout.write(result + "\n")


if __name__ == "__main__":
    main()
