import sys


def solve(input_str: str) -> str:
    lines = input_str.splitlines()
    if not lines:
        return ""

    max_len = max(len(line) for line in lines)
    padded = [line.ljust(max_len) for line in lines]

    out_lines = []
    for col in range(max_len):
        line = "".join(padded[row][col]
                       for row in range(len(padded) - 1, -1, -1))
        out_lines.append(line.rstrip())

    return "\n".join(out_lines) + "\n"


def main() -> None:
    data = sys.stdin.read()
    result = solve(data)
    if result:
        sys.stdout.write(result)


if __name__ == "__main__":
    main()
