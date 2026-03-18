def solve(data: str) -> str:
    answers: list[str] = []

    for line in data.splitlines():
        line = line.strip()
        if not line:
            continue

        parts = line.split()
        if len(parts) < 2:
            continue

        a = int(parts[0])
        b = int(parts[1])
        answers.append(str(abs(a - b)))
    return "\n".join(answers)


def main() -> None:
    import sys
    result = solve(sys.stdin.read())
    if result:
        sys.stdout.write(result + "\n")


if __name__ == "__main__":
    main()
