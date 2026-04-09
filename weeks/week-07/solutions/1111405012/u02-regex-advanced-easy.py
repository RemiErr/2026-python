from __future__ import annotations

import re
from calendar import month_abbr
from collections.abc import Callable


_DATE_PATTERN = re.compile(r"(\d+)/(\d+)/(\d+)")


def find_dates_with_module(text: str) -> list[tuple[str, str, str]]:
    return re.findall(r"(\d+)/(\d+)/(\d+)", text)


def find_dates_with_pattern(text: str) -> list[tuple[str, str, str]]:
    return _DATE_PATTERN.findall(text)


def _change_date(match: re.Match[str]) -> str:
    # 月份數字轉英文縮寫，像 11 變成 Nov。
    return f"{match.group(2)} {month_abbr[int(match.group(1))]} {match.group(3)}"


def rewrite_dates(text: str) -> str:
    return _DATE_PATTERN.sub(_change_date, text)


def matchcase(word: str) -> Callable[[re.Match[str]], str]:
    # 記法：全大寫就回全大寫，首字大寫就回首字大寫。
    def replace(match: re.Match[str]) -> str:
        original = match.group()
        if original.isupper():
            return word.upper()
        if original.islower():
            return word.lower()
        if original[0].isupper():
            return word.capitalize()
        return word

    return replace


def replace_python_word(text: str, replacement: str = "snake") -> str:
    return re.sub("python", matchcase(replacement), text, flags=re.IGNORECASE)
