from __future__ import annotations

import calendar
from datetime import datetime, timedelta


def month_keyword_error() -> str:
    try:
        timedelta(months=1)
    except TypeError as error:
        return str(error)
    raise AssertionError("timedelta unexpectedly accepted months")


def add_one_month(dt: datetime) -> datetime:
    year = dt.year
    month = dt.month + 1
    if month == 13:
        year += 1
        month = 1

    _, last_day = calendar.monthrange(year, month)
    day = min(dt.day, last_day)
    return dt.replace(year=year, month=month, day=day)


def parse_with_strptime(text: str) -> datetime:
    return datetime.strptime(text, "%Y-%m-%d")


def parse_manually(text: str) -> datetime:
    year, month, day = text.split("-")
    return datetime(int(year), int(month), int(day))
