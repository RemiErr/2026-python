from itertools import (
    chain,
    combinations,
    combinations_with_replacement,
    dropwhile,
    islice,
    permutations,
    takewhile,
)


def count(start):
    """從指定數字開始，持續往上產生整數。"""
    number = start
    while True:
        yield number
        number += 1


def slice_count(start, begin, end):
    """取出 count 生成器中的某一段資料。"""
    return list(islice(count(start), begin, end))


def drop_until_limit(numbers, limit):
    """丟掉前面小於 limit 的值，直到第一次不符合條件為止。"""
    return list(dropwhile(lambda value: value < limit, numbers))


def take_until_limit(numbers, limit):
    """持續拿取前面小於 limit 的值，一旦不符合就停止。"""
    return list(takewhile(lambda value: value < limit, numbers))


def chain_values(*iterables):
    """把多組資料接成一個串列。"""
    return list(chain(*iterables))


def get_permutations(items, length=None):
    """回傳所有排列。"""
    if length is None:
        return list(permutations(items))
    return list(permutations(items, length))


def get_combinations(items, length):
    """回傳所有組合。"""
    return list(combinations(items, length))


def password_candidates(chars, length=2):
    """使用排列做教材中的密碼窮舉示範。"""
    return ["".join(group) for group in permutations(chars, length)]


def repeated_password_candidates(chars, length=2):
    """沿用教材範例，使用可重複組合示範資料列舉。"""
    return ["".join(group) for group in combinations_with_replacement(chars, length)]


def run_examples():
    """重現原始教材中的 itertools 示範。"""
    print("--- islice() 切片 ---")
    result = slice_count(0, 5, 10)
    print(f"islice(c, 5, 10): {result}")

    print("\n--- dropwhile() 條件跳過 ---")
    nums = [1, 3, 5, 2, 4, 6]
    result = drop_until_limit(nums, 5)
    print(f"dropwhile(x<5, {nums}): {result}")

    print("\n--- takewhile() 條件取用 ---")
    result = take_until_limit(nums, 5)
    print(f"takewhile(x<5, {nums}): {result}")

    print("\n--- chain() 串聯 ---")
    a = [1, 2]
    b = [3, 4]
    c = [5]
    print(f"chain(a, b, c): {chain_values(a, b, c)}")

    print("\n--- permutations() 排列 ---")
    items = ["a", "b", "c"]
    print("permutations(items):")
    for group in get_permutations(items):
        print(f"  {group}")

    print("permutations(items, 2):")
    for group in get_permutations(items, 2):
        print(f"  {group}")

    print("\n--- combinations() 組合 ---")
    print("combinations(items, 2):")
    for group in get_combinations(items, 2):
        print(f"  {group}")

    print("\n--- 組合應用：密碼窮舉 ---")
    chars = ["A", "B", "1"]
    print("2位數密碼:")
    for group in password_candidates(chars):
        print(f"  {group}")

    print("2位數密碼（可重複）:")
    for group in repeated_password_candidates(chars):
        print(f"  {group}")


def main():
    run_examples()


if __name__ == "__main__":
    main()
