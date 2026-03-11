import sys

memo = {}


def cal(i: int) -> int:
    if i in memo:
        return memo[i]

    if i <= 1:
        return 1

    if (i % 2) ^ 1:
        memo[i] = 1 + cal(i // 2)
    else:
        memo[i] = 1 + cal(3 * i + 1)
    return memo[i]


def solve(input_str: str) -> str:
    tokens = input_str.split()
    if not tokens:
        return ""

    out = []
    for k in range(0, len(tokens) - 1, 2):
        a = int(tokens[k])
        b = int(tokens[k + 1])
        mx_len = 0
        for i in range(min(a, b), max(a, b) + 1):
            _ = cal(i)
            if _ > mx_len:
                mx_len = _
        out.append(f"{a} {b} {mx_len}")

    return "\n".join(out)


def main() -> None:
    data = sys.stdin.read()
    result = solve(data)
    if result:
        sys.stdout.write(result)


if __name__ == "__main__":
    main()
