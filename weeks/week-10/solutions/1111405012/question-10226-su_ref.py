import sys
from functools import lru_cache


def read_cases(text):
    """把整份輸入切成多筆測資。"""
    numbers = list(map(int, text.split()))
    cases = []
    index = 0

    while index < len(numbers):
        size = numbers[index]
        index += 1
        blocked = [set() for _ in range(size)]

        for person in range(size):
            while numbers[index] != 0:
                blocked[person].add(numbers[index])
                index += 1
            index += 1

        cases.append((size, blocked))

    return cases


def build_candidates(size, blocked):
    """先把每個座位可以坐哪些人整理好。"""
    candidates = []

    for seat_no in range(1, size + 1):
        seat_choices = []
        for person in range(size):
            if seat_no not in blocked[person]:
                seat_choices.append(person)
        candidates.append(seat_choices)

    return candidates


def format_incremental_output(arrangements):
    """依題目要求，只輸出和上一個排列不同的尾端。"""
    output = []
    previous = ""

    for current in arrangements:
        if not previous:
            output.append(current)
        else:
            diff = 0
            while diff < len(current) and current[diff] == previous[diff]:
                diff += 1
            output.append(current[diff:])
        previous = current

    return "\n".join(output)


def solve_one(size, blocked):
    candidates = build_candidates(size, blocked)
    names = [chr(ord("A") + person) for person in range(size)]
    full_mask = (1 << size) - 1
    arrangements = []
    path = []

    @lru_cache(maxsize=None)
    def can_finish(seat_index, used_mask):
        """先判斷剩下的座位是否還有可能填完，用來剪枝。"""
        if seat_index == size:
            return used_mask == full_mask

        for person in candidates[seat_index]:
            bit = 1 << person
            if used_mask & bit:
                continue
            if can_finish(seat_index + 1, used_mask | bit):
                return True
        return False

    def backtrack(seat_index, used_mask):
        if seat_index == size:
            arrangements.append("".join(path))
            return

        for person in candidates[seat_index]:
            bit = 1 << person
            if used_mask & bit:
                continue
            if not can_finish(seat_index + 1, used_mask | bit):
                continue

            path.append(names[person])
            backtrack(seat_index + 1, used_mask | bit)
            path.pop()

    if can_finish(0, 0):
        backtrack(0, 0)

    return format_incremental_output(arrangements)


def solve(text):
    answers = []

    for size, blocked in read_cases(text):
        answers.append(solve_one(size, blocked))

    return "\n\n".join(answers)


if __name__ == "__main__":
    sys.stdout.write(solve(sys.stdin.read()))
