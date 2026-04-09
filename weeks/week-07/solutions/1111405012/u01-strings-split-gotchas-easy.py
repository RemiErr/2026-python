from __future__ import annotations

import re
from collections.abc import Iterable


# 想保留分隔符號時，可以把分隔符號放進括號。
_SPLIT_PATTERN = re.compile(r"(;|,|\s)\s*")


def split_preserving_delimiters(text: str) -> tuple[list[str], list[str]]:
    parts = _SPLIT_PATTERN.split(text)
    return parts[::2], parts[1::2]


def rebuild_text(values: list[str], delimiters: list[str]) -> str:
    # 把資料和分隔符號一組一組接回去。
    return "".join(value + delimiter for value, delimiter in zip(values, delimiters + [""]))


def safe_startswith(text: str, prefixes: Iterable[str]) -> bool:
    # 記法：list 不行，tuple 可以。
    return text.startswith(tuple(prefixes))


def normalize_spaces(text: str) -> str:
    # 頭尾用 strip()，中間空白用 re.sub()。
    return re.sub(r"\s+", " ", text.strip())


def clean_lines(lines: Iterable[str]) -> list[str]:
    return [line.strip() for line in lines]
