"""UVA 10035 簡單版：逐位相加，計算總共發生幾次進位。"""

from __future__ import annotations


def count_carry(a: int, b: int) -> int:
    # carry 表示「上一位有沒有進位到這一位」。
    carry = 0

    # carry_count 用來統計總共出現幾次進位。
    carry_count = 0

    # 只要任一個數字還有位數沒處理，就繼續往前算。
    while a > 0 or b > 0:
        # 用 % 10 取出目前個位數，再把上一位的進位加進來。
        total = (a % 10) + (b % 10) + carry

        if total >= 10:
            carry = 1
            carry_count += 1
        else:
            carry = 0

        # 用 // 10 去掉已經處理過的個位數。
        a //= 10
        b //= 10

    return carry_count


def solve(data: str) -> str:
    answers: list[str] = []

    for line in data.splitlines():
        line = line.strip()
        if not line:
            continue

        parts = line.split()
        if len(parts) < 2:
            continue

        a = int(parts[0])
        b = int(parts[1])

        # 0 0 代表輸入結束，不需要再往下處理。
        if a == 0 and b == 0:
            break

        carry_count = count_carry(a, b)

        # 依照題目指定的英文句型輸出。
        if carry_count == 0:
            answers.append("No carry operation.")
        elif carry_count == 1:
            answers.append("1 carry operation.")
        else:
            answers.append(f"{carry_count} carry operations.")

    return "\n".join(answers)


def main() -> None:
    import sys

    result = solve(sys.stdin.read())
    if result:
        sys.stdout.write(result + "\n")


if __name__ == "__main__":
    main()
