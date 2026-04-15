from math import isqrt
from sys import stdin, stdout


def min_sum_of_b_and_c(value_of_a):
    """由公式推導出 (b-a)(c-a) = a^2 + 1，再找最接近平方根的因數。"""
    product = value_of_a * value_of_a + 1
    factor = isqrt(product)

    while product % factor != 0:
        factor -= 1

    other_factor = product // factor
    return 2 * value_of_a + factor + other_factor


def solve(text):
    """題目只有一個正整數 a，輸出最小的 b+c。"""
    tokens = text.split()
    if not tokens:
        return ""

    value_of_a = int(tokens[0])
    return str(min_sum_of_b_and_c(value_of_a))


def main():
    result = solve(stdin.read())
    if result:
        stdout.write(result)


if __name__ == "__main__":
    main()
