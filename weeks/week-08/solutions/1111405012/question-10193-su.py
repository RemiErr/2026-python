from math import isqrt
from sys import stdin, stdout


def main():
    data = stdin.read().split()
    if not data:
        return

    a = int(data[0])
    num = a * a + 1

    x = isqrt(num)
    while num % x != 0:
        x -= 1

    y = num // x
    answer = 2 * a + x + y
    stdout.write(str(answer))


if __name__ == "__main__":
    main()
