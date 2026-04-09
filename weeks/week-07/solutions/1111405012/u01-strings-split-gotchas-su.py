from __future__ import annotations

import re
from collections.abc import Iterable


_SPLIT_PATTERN = re.compile(r"(;|,|\s)\s*")


def split_preserving_delimiters(text: str) -> tuple[list[str], list[str]]:
    parts = _SPLIT_PATTERN.split(text)
    return parts[::2], parts[1::2]


def rebuild_text(values: list[str], delimiters: list[str]) -> str:
    return "".join(value + delimiter for value, delimiter in zip(values, delimiters + [""]))


def safe_startswith(text: str, prefixes: Iterable[str]) -> bool:
    return text.startswith(tuple(prefixes))


def normalize_spaces(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip())


def clean_lines(lines: Iterable[str]) -> list[str]:
    return [line.strip() for line in lines]
