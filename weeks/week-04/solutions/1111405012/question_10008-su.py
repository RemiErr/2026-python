def solve(data: str) -> str:
    lines = data.splitlines()
    if not lines:
        return ""
    n = int(lines[0].strip() or "0")
    count: dict[str, int] = {}
    for i in range(1, min(n + 1, len(lines))):
        line = lines[i].upper()

        for ch in line:
            if "A" <= ch <= "Z":
                count[ch] = count.get(ch, 0) + 1

    items = list(count.items())
    items.sort(key=lambda item: (-item[1], item[0]))

    answer_lines: list[str] = []
    for letter, times in items:
        answer_lines.append(f"{letter} {times}")

    return "\n".join(answer_lines)


def main() -> None:
    import sys

    result = solve(sys.stdin.read())
    if result:
        sys.stdout.write(result + "\n")


if __name__ == "__main__":
    main()
