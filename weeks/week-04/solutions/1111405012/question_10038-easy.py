"""UVA 10038 簡單版：檢查相鄰差值是否剛好包含 1 到 n-1。"""

from __future__ import annotations


def is_jolly(sequence: list[int]) -> bool:
    n = len(sequence)

    # 只有 1 個數字時，依題意一定是 Jolly。
    if n <= 1:
        return True

    # seen[d] 代表差值 d 有沒有出現過。
    # 我們只會用到 1 到 n-1，所以長度開成 n 就夠了。
    seen = [False] * n

    for i in range(1, n):
        diff = abs(sequence[i] - sequence[i - 1])

        # 合法差值只能落在 1 到 n-1。
        # 只要超出範圍，這串數列就不可能是 Jolly。
        if diff <= 0 or diff >= n:
            return False

        seen[diff] = True

    # 最後檢查 1 到 n-1 是否每個差值都出現過。
    for diff in range(1, n):
        if not seen[diff]:
            return False

    return True


def solve(data: str) -> str:
    answers: list[str] = []

    for line in data.splitlines():
        line = line.strip()
        if not line:
            continue

        numbers = list(map(int, line.split()))
        if not numbers:
            continue

        # 第 1 個數字是長度，後面才是真正的數列內容。
        n = numbers[0]
        sequence = numbers[1 : 1 + n]

        if is_jolly(sequence):
            answers.append("Jolly")
        else:
            answers.append("Not jolly")

    return "\n".join(answers)


def main() -> None:
    import sys

    result = solve(sys.stdin.read())
    if result:
        sys.stdout.write(result + "\n")


if __name__ == "__main__":
    main()
