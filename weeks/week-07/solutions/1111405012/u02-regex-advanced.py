from __future__ import annotations

import re
from calendar import month_abbr
from collections.abc import Callable


# 把日期規則先編譯好，之後找日期與取代日期都能共用。
_DATE_PATTERN = re.compile(r"(\d+)/(\d+)/(\d+)")


def find_dates_with_module(text: str) -> list[tuple[str, str, str]]:
    # 直接用 re.findall()，適合一次性操作。
    return re.findall(r"(\d+)/(\d+)/(\d+)", text)


def find_dates_with_pattern(text: str) -> list[tuple[str, str, str]]:
    # 已編譯好的 pattern 可以重複利用。
    return _DATE_PATTERN.findall(text)


def _change_date(match: re.Match[str]) -> str:
    # 把數字月份改成英文縮寫月份。
    month_text = month_abbr[int(match.group(1))]
    day_text = match.group(2)
    year_text = match.group(3)
    return f"{day_text} {month_text} {year_text}"


def rewrite_dates(text: str) -> str:
    # sub() 可以搭配函式，依照每一個 match 動態產生新字串。
    return _DATE_PATTERN.sub(_change_date, text)


def matchcase(word: str) -> Callable[[re.Match[str]], str]:
    # 回傳一個 replace 函式，讓替換字能跟著原字大小寫變化。
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
    # 忽略大小寫搜尋，再用 matchcase() 保留原本的大小寫風格。
    return re.sub("python", matchcase(replacement), text, flags=re.IGNORECASE)
