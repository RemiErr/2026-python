def count_carry(a: int, b: int) -> int:
    carry = 0
    carry_count = 0
    while a > 0 or b > 0:
        total = (a % 10) + (b % 10) + carry

        if total >= 10:
            carry = 1
            carry_count += 1
        else:
            carry = 0
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

        if a == 0 and b == 0:
            break

        carry_count = count_carry(a, b)

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
