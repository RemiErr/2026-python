import sys
from functools import lru_cache


def split_cases(text):
    nums = list(map(int, text.split()))
    pos = 0
    cases = []

    while pos < len(nums):
        n = nums[pos]
        pos += 1
        bad = [set() for _ in range(n)]

        for person in range(n):
            while True:
                seat = nums[pos]
                pos += 1
                if seat == 0:
                    break
                bad[person].add(seat)

        cases.append((n, bad))

    return cases


def make_allowed(n, bad):
    allowed = [0] * n

    for seat_index in range(n):
        seat_no = seat_index + 1
        mask = 0

        for person in range(n):
            if seat_no not in bad[person]:
                mask |= 1 << person

        allowed[seat_index] = mask

    return allowed


def solve_one(n, bad):
    allowed = make_allowed(n, bad)
    names = [chr(65 + i) for i in range(n)]
    full_mask = (1 << n) - 1
    path = []
    out = []
    last = ""

    # 先記住哪些狀態還有機會排完，DFS 就能少走很多冤枉路。
    @lru_cache(maxsize=None)
    def ok(seat_index, used):
        if seat_index == n:
            return used == full_mask

        choices = allowed[seat_index] & ~used
        while choices:
            pick = choices & -choices
            if ok(seat_index + 1, used | pick):
                return True
            choices -= pick
        return False

    def dfs(seat_index, used):
        nonlocal last

        if seat_index == n:
            now = "".join(path)
            if not last:
                out.append(now)
            else:
                diff = 0
                while diff < n and now[diff] == last[diff]:
                    diff += 1
                out.append(now[diff:])
            last = now
            return

        choices = allowed[seat_index] & ~used
        while choices:
            pick = choices & -choices
            person = pick.bit_length() - 1

            if ok(seat_index + 1, used | pick):
                path.append(names[person])
                dfs(seat_index + 1, used | pick)
                path.pop()

            choices -= pick

    if ok(0, 0):
        dfs(0, 0)

    return "\n".join(out)


def solve(text):
    pieces = []
    for n, bad in split_cases(text):
        pieces.append(solve_one(n, bad))
    return "\n\n".join(pieces)


if __name__ == "__main__":
    sys.stdout.write(solve(sys.stdin.read()))
