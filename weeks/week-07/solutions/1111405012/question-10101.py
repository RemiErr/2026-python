from __future__ import annotations

from dataclasses import dataclass
import sys


DIGIT_MASKS = (
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

SAME_MOVE: list[list[int]] = [[] for _ in range(10)]
LOSE_ONE: list[list[int]] = [[] for _ in range(10)]
GAIN_ONE: list[list[int]] = [[] for _ in range(10)]

for old_digit, old_mask in enumerate(DIGIT_MASKS):
    for new_digit, new_mask in enumerate(DIGIT_MASKS):
        diff_bits = (old_mask ^ new_mask).bit_count()
        if diff_bits == 2 and old_mask.bit_count() == new_mask.bit_count():
            SAME_MOVE[old_digit].append(new_digit)
        if diff_bits == 1 and new_mask & old_mask == new_mask:
            LOSE_ONE[old_digit].append(new_digit)
        if diff_bits == 1 and new_mask & old_mask == old_mask:
            GAIN_ONE[old_digit].append(new_digit)


@dataclass(frozen=True)
class DigitInfo:
    position: int
    digit: int
    coefficient: int


def collect_digits(expression: str) -> list[DigitInfo]:
    left_side, right_side = expression.split("=")
    return parse_side(left_side, 0, 1) + parse_side(right_side, len(left_side) + 1, -1)


def parse_side(text: str, offset: int, side_sign: int) -> list[DigitInfo]:
    result: list[DigitInfo] = []
    index = 0
    current_sign = 1

    if text and text[0] in "+-":
        current_sign = -1 if text[0] == "-" else 1
        index = 1

    while index < len(text):
        start = index
        while index < len(text) and text[index].isdigit():
            index += 1

        number = text[start:index]
        place_value = 10 ** (len(number) - 1)
        number_sign = side_sign * current_sign

        for digit_index, char in enumerate(number):
            result.append(
                DigitInfo(
                    position=offset + start + digit_index,
                    digit=int(char),
                    coefficient=number_sign * place_value,
                )
            )
            place_value //= 10

        if index < len(text):
            current_sign = 1 if text[index] == "+" else -1
            index += 1

    return result


def replace_digits(expression: str, changes: list[tuple[int, int]]) -> str:
    chars = list(expression)
    for position, new_digit in changes:
        chars[position] = str(new_digit)
    return "".join(chars) + "#"


def solve(data: str) -> str:
    if "#" not in data:
        return "No"

    expression = data.split("#", 1)[0].strip()
    if not expression:
        return "No"

    digits = collect_digits(expression)
    balance = sum(info.coefficient * info.digit for info in digits)

    # 先找「同一個數字內部挪一根火柴」的情況。
    for info in digits:
        for new_digit in SAME_MOVE[info.digit]:
            delta = info.coefficient * (new_digit - info.digit)
            if balance + delta == 0:
                return replace_digits(expression, [(info.position, new_digit)])

    # 再找「一個數字少一根，另一個數字多一根」的情況。
    gain_map: dict[int, list[tuple[int, int]]] = {}
    for info in digits:
        for new_digit in GAIN_ONE[info.digit]:
            delta = info.coefficient * (new_digit - info.digit)
            gain_map.setdefault(delta, []).append((info.position, new_digit))

    for info in digits:
        for new_digit in LOSE_ONE[info.digit]:
            loss_delta = info.coefficient * (new_digit - info.digit)
            need = -balance - loss_delta
            for gain_position, gain_digit in gain_map.get(need, []):
                if gain_position == info.position:
                    continue
                return replace_digits(
                    expression,
                    [(info.position, new_digit), (gain_position, gain_digit)],
                )

    return "No"


def main() -> None:
    sys.stdout.write(solve(sys.stdin.read()))


if __name__ == "__main__":
    main()
