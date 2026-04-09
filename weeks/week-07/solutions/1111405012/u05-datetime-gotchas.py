from __future__ import annotations

import calendar
from datetime import datetime, timedelta


def month_keyword_error() -> str:
    # timedelta 不支援 months 參數，這裡把錯誤訊息留下來方便教學。
    try:
        timedelta(months=1)
    except TypeError as error:
        return str(error)
    raise AssertionError("timedelta unexpectedly accepted months")


def add_one_month(dt: datetime) -> datetime:
    # 先算出目標年月。
    target_year = dt.year
    target_month = dt.month + 1
    if target_month == 13:
        target_year += 1
        target_month = 1

    # 目標月份天數若比較少，就把日期壓到最後一天。
    _, last_day = calendar.monthrange(target_year, target_month)
    target_day = min(dt.day, last_day)
    return dt.replace(year=target_year, month=target_month, day=target_day)


def parse_with_strptime(text: str) -> datetime:
    # 這是最常見、可讀性高的寫法。
    return datetime.strptime(text, "%Y-%m-%d")


def parse_manually(text: str) -> datetime:
    # 結構固定時，也可以自己 split 再轉型。
    year_text, month_text, day_text = text.split("-")
    return datetime(int(year_text), int(month_text), int(day_text))
