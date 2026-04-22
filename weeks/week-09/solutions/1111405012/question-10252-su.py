import sys


def solve(text):
    nums = list(map(int, text.split()))
    if not nums:
        return ""

    pos = 0
    t = nums[pos]
    pos += 1
    out = []

    for _ in range(t):
        n = nums[pos]
        pos += 1
        xs = []
        ys = []

        for _ in range(n):
            xs.append(nums[pos])
            ys.append(nums[pos + 1])
            pos += 2

        xs.sort()
        ys.sort()

        x1 = xs[(n - 1) // 2]
        x2 = xs[n // 2]
        y1 = ys[(n - 1) // 2]
        y2 = ys[n // 2]

        best = sum(abs(x - x1) for x in xs) + sum(abs(y - y1) for y in ys)
        count = (x2 - x1 + 1) * (y2 - y1 + 1)
        out.append(f"{best} {count}")

    return "\n".join(out)


if __name__ == "__main__":
    sys.stdout.write(solve(sys.stdin.read()))
