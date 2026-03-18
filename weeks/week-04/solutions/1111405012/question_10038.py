"""UVA 10038 Jolly Jumpers 解法，判斷序列是否為 Jolly。"""

from __future__ import annotations


def is_jolly(sequence: list[int]) -> bool:
    n = len(sequence)
    if n <= 1:
        return True

    # 收集相鄰元素差的絕對值，Jolly 序列必須剛好包含 1 到 n-1。
    diffs = {abs(sequence[i] - sequence[i - 1]) for i in range(1, n)}
    return diffs == set(range(1, n))


def solve(data: str) -> str:
    outputs: list[str] = []

    for line in data.splitlines():
        if not line.strip():
            continue

        numbers = list(map(int, line.split()))
        if not numbers:
            continue

        # 第一個數字是序列長度，後面才是真正的序列內容。
        n = numbers[0]
        sequence = numbers[1 : 1 + n]
        outputs.append("Jolly" if is_jolly(sequence) else "Not jolly")

    return "\n".join(outputs)


def main() -> None:
    import sys

    result = solve(sys.stdin.read())
    if result:
        sys.stdout.write(result + "\n")


if __name__ == "__main__":
    main()
