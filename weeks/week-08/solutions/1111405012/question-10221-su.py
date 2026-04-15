import math
from sys import stdin, stdout


def main():
    data = stdin.read().split()
    i = 0
    out = []

    while i + 2 < len(data):
        s = float(data[i])
        a = float(data[i + 1])
        unit = data[i + 2]
        i += 3

        if unit == "min":
            a /= 60.0

        a %= 360.0
        if a > 180.0:
            a = 360.0 - a

        radius = 6440.0 + s
        rad = math.radians(a)

        arc = radius * rad
        chord = 2.0 * radius * math.sin(rad / 2.0)

        out.append(f"{arc:.6f} {chord:.6f}")

    stdout.write("\n".join(out))


if __name__ == "__main__":
    main()
