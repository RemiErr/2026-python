from __future__ import annotations

import re
from collections.abc import Iterable


# 先把規則編譯好，重複使用時會比較直覺。
_SPLIT_PATTERN = re.compile(r"(;|,|\s)\s*")


def split_preserving_delimiters(text: str) -> tuple[list[str], list[str]]:
    # re.split() 搭配捕獲分組時，分隔符號也會一起留下來。
    pieces = _SPLIT_PATTERN.split(text)

    # 偶數位置是資料，奇數位置是分隔符號。
    values = pieces[::2]
    delimiters = pieces[1::2]
    return values, delimiters


def rebuild_text(values: list[str], delimiters: list[str]) -> str:
    # 最後一個值後面沒有分隔符號，所以補一個空字串。
    full_delimiters = delimiters + [""]
    return "".join(value + delimiter for value, delimiter in zip(values, full_delimiters))


def safe_startswith(text: str, prefixes: Iterable[str]) -> bool:
    # str.startswith() 只能吃單一字串或 tuple。
    return text.startswith(tuple(prefixes))


def normalize_spaces(text: str) -> str:
    # strip() 只會清頭尾，所以中間的連續空白要再用正則壓成一個。
    trimmed = text.strip()
    return re.sub(r"\s+", " ", trimmed)


def clean_lines(lines: Iterable[str]) -> list[str]:
    # 逐行去掉頭尾空白，適合處理讀檔後的每一列文字。
    return [line.strip() for line in lines]
