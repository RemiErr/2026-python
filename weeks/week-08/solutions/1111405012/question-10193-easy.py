from math import isqrt
from sys import stdin, stdout


def main():
    data = stdin.read().split()
    if not data:
        return

    a = int(data[0])

    # 由 arctan 加法公式可以整理成：
    # (b - a) * (c - a) = a^2 + 1
    # 所以只要把 a^2 + 1 拆成兩個因數，就能得到 b 和 c。
    num = a * a + 1

    # 想讓 b + c 最小，就要讓兩個因數盡量接近。
    x = isqrt(num)
    while num % x != 0:
        x -= 1

    y = num // x
    answer = 2 * a + x + y
    stdout.write(str(answer))


if __name__ == "__main__":
    main()
