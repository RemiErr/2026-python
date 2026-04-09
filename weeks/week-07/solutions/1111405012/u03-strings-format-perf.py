from __future__ import annotations

from collections.abc import Mapping


class SafeSub(dict[str, object]):
    # format_map() 找不到鍵時，改成保留原本的佔位符。
    def __missing__(self, key: str) -> str:
        return "{" + key + "}"


def concat_with_plus(parts: list[str]) -> str:
    # 一段一段往後加，寫法直覺，但大量字串時效率較差。
    result = ""
    for part in parts:
        result += part
    return result


def concat_with_join(parts: list[str]) -> str:
    # join() 會一次把所有片段接好，通常比較適合組字串。
    return "".join(parts)


def safe_format(template: str, mapping: Mapping[str, object]) -> str:
    # 先把資料包成 SafeSub，再交給 format_map()。
    return template.format_map(SafeSub(mapping))


def first_text_character(text: str) -> str:
    # 字串索引回傳的還是字元。
    return text[0]


def first_byte_value(data: bytes) -> int:
    # bytes 索引回傳的是整數，不是單字元字串。
    return data[0]


def format_to_ascii_bytes(name: str, count: int) -> bytes:
    # 先把字串格式化，再 encode 成 bytes。
    return "{:10s} {:5d}".format(name, count).encode("ascii")
