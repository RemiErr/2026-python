from __future__ import annotations

from dataclasses import dataclass
import sys


MASKS = (
    0b1111110,
    0b0110000,
    0b1101101,
    0b1111001,
    0b0110011,
    0b1011011,
    0b1011111,
    0b1110000,
    0b1111111,
    0b1111011,
)

MOVE_INSIDE = [[] for _ in range(10)]
TAKE_ONE = [[] for _ in range(10)]
ADD_ONE = [[] for _ in range(10)]

for a, mask_a in enumerate(MASKS):
    for b, mask_b in enumerate(MASKS):
        diff = (mask_a ^ mask_b).bit_count()
        if diff == 2 and mask_a.bit_count() == mask_b.bit_count():
            MOVE_INSIDE[a].append(b)
        if diff == 1 and mask_b & mask_a == mask_b:
            TAKE_ONE[a].append(b)
        if diff == 1 and mask_b & mask_a == mask_a:
            ADD_ONE[a].append(b)


@dataclass(frozen=True)
class DigitData:
    pos: int
    num: int
    weight: int


def split_digits(expr: str) -> list[DigitData]:
    left, right = expr.split("=")
    return read_side(left, 0, 1) + read_side(right, len(left) + 1, -1)


def read_side(text: str, offset: int, side_sign: int) -> list[DigitData]:
    result: list[DigitData] = []
    i = 0
    sign = 1

    if text and text[0] in "+-":
        sign = -1 if text[0] == "-" else 1
        i = 1

    while i < len(text):
        start = i
        while i < len(text) and text[i].isdigit():
            i += 1
        number = text[start:i]
        base = 10 ** (len(number) - 1)
        total_sign = side_sign * sign
        for j, ch in enumerate(number):
            result.append(DigitData(offset + start + j, int(ch), total_sign * base))
            base //= 10
        if i < len(text):
            sign = 1 if text[i] == "+" else -1
            i += 1

    return result


def change(expr: str, edits: list[tuple[int, int]]) -> str:
    chars = list(expr)
    for pos, digit in edits:
        chars[pos] = str(digit)
    return "".join(chars) + "#"


def solve(data: str) -> str:
    if "#" not in data:
        return "No"

    expr = data.split("#", 1)[0].strip()
    if not expr:
        return "No"

    digits = split_digits(expr)
    now = sum(item.weight * item.num for item in digits)

    # 先試只改一個數字，把同一根火柴移到這個數字的別段上。
    for item in digits:
        for nxt in MOVE_INSIDE[item.num]:
            if now + item.weight * (nxt - item.num) == 0:
                return change(expr, [(item.pos, nxt)])

    # 再試一個數字拿出一根，另一個數字補進一根。
    plus_map: dict[int, list[tuple[int, int]]] = {}
    for item in digits:
        for nxt in ADD_ONE[item.num]:
            delta = item.weight * (nxt - item.num)
            plus_map.setdefault(delta, []).append((item.pos, nxt))

    for item in digits:
        for nxt in TAKE_ONE[item.num]:
            lose = item.weight * (nxt - item.num)
            target = -now - lose
            for pos2, nxt2 in plus_map.get(target, []):
                if pos2 == item.pos:
                    continue
                return change(expr, [(item.pos, nxt), (pos2, nxt2)])

    return "No"


def main() -> None:
    sys.stdout.write(solve(sys.stdin.read()))


if __name__ == "__main__":
    main()
