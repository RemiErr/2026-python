from __future__ import annotations

from collections.abc import Mapping


class SafeSub(dict[str, object]):
    def __missing__(self, key: str) -> str:
        return "{" + key + "}"


def concat_with_plus(parts: list[str]) -> str:
    result = ""
    for part in parts:
        result += part
    return result


def concat_with_join(parts: list[str]) -> str:
    return "".join(parts)


def safe_format(template: str, mapping: Mapping[str, object]) -> str:
    return template.format_map(SafeSub(mapping))


def first_text_character(text: str) -> str:
    return text[0]


def first_byte_value(data: bytes) -> int:
    return data[0]


def format_to_ascii_bytes(name: str, count: int) -> bytes:
    return "{:10s} {:5d}".format(name, count).encode("ascii")
