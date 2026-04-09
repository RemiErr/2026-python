from __future__ import annotations

import math
from decimal import Decimal, ROUND_HALF_UP


def bankers_round(value: float, digits: int = 0) -> int | float:
    # Python 內建 round() 走的是銀行家捨入。
    return round(value, digits)


def traditional_round(value: float, digits: int = 0) -> Decimal:
    # 想要日常常見的四捨五入，可以改用 Decimal。
    decimal_value = Decimal(str(value))
    quantizer = Decimal("1") if digits == 0 else Decimal("0." + "0" * digits)
    return decimal_value.quantize(quantizer, rounding=ROUND_HALF_UP)


def is_nan(value: float) -> bool:
    # NaN 不能用 == 判斷，要交給 math.isnan()。
    return math.isnan(value)


def remove_nan(values: list[float]) -> list[float]:
    # 把所有不是 NaN 的數字留下來。
    return [value for value in values if not math.isnan(value)]


def float_sum() -> float:
    # float 很快，但有時會出現二進位浮點誤差。
    return 0.1 + 0.2


def decimal_sum() -> Decimal:
    # Decimal 用字串建立，可保留十進位精度。
    return Decimal("0.1") + Decimal("0.2")


def float_equals_point_three() -> bool:
    return float_sum() == 0.3


def decimal_equals_point_three() -> bool:
    return decimal_sum() == Decimal("0.3")
