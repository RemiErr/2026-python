from __future__ import annotations

from collections.abc import Iterable
from typing import Any


def consume_with_next(items: Iterable[Any]) -> list[Any]:
    result: list[Any] = []
    iterator = iter(items)
    while True:
        try:
            result.append(next(iterator))
        except StopIteration:
            break
    return result


def consume_with_default(items: Iterable[Any]) -> list[Any]:
    result: list[Any] = []
    iterator = iter(items)
    sentinel = object()
    while True:
        item = next(iterator, sentinel)
        if item is sentinel:
            break
        result.append(item)
    return result


class CountDown:
    def __init__(self, start: int) -> None:
        self.start = start

    def __iter__(self) -> "CountDownIterator":
        return CountDownIterator(self.start)


class CountDownIterator:
    def __init__(self, start: int) -> None:
        self.current = start

    def __iter__(self) -> "CountDownIterator":
        return self

    def __next__(self) -> int:
        if self.current <= 0:
            raise StopIteration
        value = self.current
        self.current -= 1
        return value


def is_iterable(value: Any) -> bool:
    try:
        iter(value)
    except TypeError:
        return False
    return True


def is_iterator(value: Any) -> bool:
    return hasattr(value, "__iter__") and hasattr(value, "__next__")
