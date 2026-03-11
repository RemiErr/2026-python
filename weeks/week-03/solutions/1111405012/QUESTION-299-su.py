import sys


def solve(input_str: str) -> str:
    tokens = input_str.split()
    if not tokens:
        return ""

    t = int(tokens[0])
    idx = 1
    out = []

    for _ in range(t):
        l = int(tokens[idx])
        idx += 1
        arr = list(map(int, tokens[idx: idx + l]))
        idx += l

        swaps = 0
        for i in range(l):
            for j in range(l - 1 - i):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    swaps += 1

        out.append(f"Optimal train swapping takes {swaps} swaps.")

    return "\n".join(out)


def main() -> None:
    data = sys.stdin.read()
    result = solve(data)
    if result:
        sys.stdout.write(result)


if __name__ == "__main__":
    main()
