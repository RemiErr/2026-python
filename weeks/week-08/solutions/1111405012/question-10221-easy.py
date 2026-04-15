import math
from sys import stdin, stdout


def main():
    # 每筆資料會給高度 s、角度 a，以及角度單位。
    data = stdin.read().split()
    i = 0
    out = []

    while i + 2 < len(data):
        s = float(data[i])
        a = float(data[i + 1])
        unit = data[i + 2]
        i += 3

        # 如果是角分，就先換成角度。
        if unit == "min":
            a /= 60.0

        # 同一段圓弧，超過 180 度就改走另一邊較短的那段。
        a %= 360.0
        if a > 180.0:
            a = 360.0 - a

        radius = 6440.0 + s
        rad = math.radians(a)

        # 弧長 = 半徑 * 弧度；弦長 = 2 * r * sin(角度 / 2)。
        arc = radius * rad
        chord = 2.0 * radius * math.sin(rad / 2.0)

        out.append(f"{arc:.6f} {chord:.6f}")

    stdout.write("\n".join(out))


if __name__ == "__main__":
    main()
