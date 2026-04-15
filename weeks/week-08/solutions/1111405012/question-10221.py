import math
from sys import stdin, stdout


EARTH_RADIUS = 6440.0


def solve(text):
    """根據高度與角度，計算弧長與弦長。"""
    tokens = text.split()
    outputs = []

    for index in range(0, len(tokens) - 2, 3):
        surface_height = float(tokens[index])
        angle = float(tokens[index + 1])
        unit = tokens[index + 2]

        if unit == "min":
            angle /= 60.0

        angle %= 360.0
        if angle > 180.0:
            angle = 360.0 - angle

        radius = EARTH_RADIUS + surface_height
        radians = math.radians(angle)

        arc_length = radius * radians
        chord_length = 2.0 * radius * math.sin(radians / 2.0)

        outputs.append(f"{arc_length:.6f} {chord_length:.6f}")

    return "\n".join(outputs)


def main():
    result = solve(stdin.read())
    if result:
        stdout.write(result)


if __name__ == "__main__":
    main()
