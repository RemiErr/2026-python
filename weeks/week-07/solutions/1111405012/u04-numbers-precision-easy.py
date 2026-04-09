from __future__ import annotations

import math
from decimal import Decimal, ROUND_HALF_UP


def bankers_round(value: float, digits: int = 0) -> int | float:
    return round(value, digits)


def traditional_round(value: float, digits: int = 0) -> Decimal:
    # 想記住傳統四捨五入：Decimal + ROUND_HALF_UP。
    number = Decimal(str(value))
    unit = Decimal("1") if digits == 0 else Decimal("0." + "0" * digits)
    return number.quantize(unit, rounding=ROUND_HALF_UP)


def is_nan(value: float) -> bool:
    return math.isnan(value)


def remove_nan(values: list[float]) -> list[float]:
    return [value for value in values if not math.isnan(value)]


def float_sum() -> float:
    return 0.1 + 0.2


def decimal_sum() -> Decimal:
    return Decimal("0.1") + Decimal("0.2")


def float_equals_point_three() -> bool:
    return float_sum() == 0.3


def decimal_equals_point_three() -> bool:
    return decimal_sum() == Decimal("0.3")
