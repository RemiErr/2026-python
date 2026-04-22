import sys


LIMIT = 63
MAX_K = 100


def make_dp():
    dp = [[0] * (MAX_K + 1) for _ in range(LIMIT + 1)]

    for moves in range(1, LIMIT + 1):
        for eggs in range(1, MAX_K + 1):
            dp[moves][eggs] = dp[moves - 1][eggs - 1] + dp[moves - 1][eggs] + 1

    return dp


DP = make_dp()


def solve(text):
    out = []

    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue

        k, n = map(int, line.split())
        if k == 0:
            break

        ans = "More than 63 trials needed."
        for moves in range(1, LIMIT + 1):
            if DP[moves][k] >= n:
                ans = str(moves)
                break

        out.append(ans)

    return "\n".join(out)


if __name__ == "__main__":
    sys.stdout.write(solve(sys.stdin.read()))
