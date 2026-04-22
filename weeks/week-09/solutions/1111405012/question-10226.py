import sys
from functools import lru_cache


def read_cases(text):
    numbers = list(map(int, text.split()))
    index = 0
    cases = []

    while index < len(numbers):
        people_count = numbers[index]
        index += 1
        forbidden_positions = [set() for _ in range(people_count)]

        for person_index in range(people_count):
            while True:
                position = numbers[index]
                index += 1
                if position == 0:
                    break
                forbidden_positions[person_index].add(position)

        cases.append((people_count, forbidden_positions))

    return cases


def build_allowed_masks(people_count, forbidden_positions):
    allowed_masks = [0] * people_count

    for position_index in range(people_count):
        mask = 0
        position_number = position_index + 1

        for person_index in range(people_count):
            if position_number not in forbidden_positions[person_index]:
                mask |= 1 << person_index

        allowed_masks[position_index] = mask

    return allowed_masks


def solve_case(people_count, forbidden_positions):
    allowed_masks = build_allowed_masks(people_count, forbidden_positions)
    all_used_mask = (1 << people_count) - 1
    letters = [chr(ord("A") + person_index) for person_index in range(people_count)]
    answers = []
    current_order = []
    previous_order = ""

    # 先判斷某個狀態之後還有沒有機會排完，避免 DFS 走進死路。
    @lru_cache(maxsize=None)
    def can_finish(position_index, used_mask):
        if position_index == people_count:
            return used_mask == all_used_mask

        choices = allowed_masks[position_index] & ~used_mask
        while choices:
            pick = choices & -choices
            if can_finish(position_index + 1, used_mask | pick):
                return True
            choices -= pick

        return False

    def dfs(position_index, used_mask):
        nonlocal previous_order

        if position_index == people_count:
            order = "".join(current_order)
            if not previous_order:
                answers.append(order)
            else:
                diff_index = 0
                while diff_index < people_count and order[diff_index] == previous_order[diff_index]:
                    diff_index += 1
                answers.append(order[diff_index:])
            previous_order = order
            return

        choices = allowed_masks[position_index] & ~used_mask
        while choices:
            pick = choices & -choices
            person_index = pick.bit_length() - 1

            if can_finish(position_index + 1, used_mask | pick):
                current_order.append(letters[person_index])
                dfs(position_index + 1, used_mask | pick)
                current_order.pop()

            choices -= pick

    if can_finish(0, 0):
        dfs(0, 0)

    return "\n".join(answers)


def solve(text):
    cases = read_cases(text)
    results = [solve_case(people_count, forbidden_positions) for people_count, forbidden_positions in cases]
    return "\n\n".join(results)


if __name__ == "__main__":
    sys.stdout.write(solve(sys.stdin.read()))
