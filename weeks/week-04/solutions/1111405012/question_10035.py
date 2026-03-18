"""UVA 10035 Primary Arithmetic 解法，計算加法中的進位次數。"""

from __future__ import annotations


def count_carry_operations(a: int, b: int) -> int:
    carry = 0
    total = 0

    while a > 0 or b > 0:
        # 逐位相加，並把上一位的進位一併算進來。
        digit_sum = (a % 10) + (b % 10) + carry
        if digit_sum >= 10:
            total += 1
            carry = 1
        else:
            carry = 0

        # 去掉已處理過的個位數，繼續檢查下一位。
        a //= 10
        b //= 10

    return total


def solve(data: str) -> str:
    outputs: list[str] = []

    for line in data.splitlines():
        if not line.strip():
            continue
        parts = line.split()
        if len(parts) < 2:
            continue

        a, b = int(parts[0]), int(parts[1])
        if a == 0 and b == 0:
            break

        carries = count_carry_operations(a, b)
        # 依題目要求輸出對應的英文句型。
        if carries == 0:
            outputs.append("No carry operation.")
        elif carries == 1:
            outputs.append("1 carry operation.")
        else:
            outputs.append(f"{carries} carry operations.")

    return "\n".join(outputs)


def main() -> None:
    import sys

    result = solve(sys.stdin.read())
    if result:
        sys.stdout.write(result + "\n")


if __name__ == "__main__":
    main()
