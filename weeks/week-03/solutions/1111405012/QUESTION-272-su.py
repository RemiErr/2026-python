import sys


def solve(input_str: str) -> str:
    out = []
    is_open = True

    for ch in input_str:
        if ch == '"':
            out.append("``" if is_open else "''")
            is_open = not is_open
        else:
            out.append(ch)

    return "".join(out)


def main() -> None:
    data = sys.stdin.read()
    result = solve(data)
    if result:
        sys.stdout.write(result)


if __name__ == "__main__":
    main()
