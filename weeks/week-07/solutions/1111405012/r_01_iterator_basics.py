from __future__ import annotations

from collections.abc import Iterable
from typing import Any


def consume_with_next(items: Iterable[Any]) -> list[Any]:
    # 直接手動呼叫 next()，直到遇到 StopIteration 為止。
    iterator = iter(items)
    collected: list[Any] = []

    while True:
        try:
            collected.append(next(iterator))
        except StopIteration:
            break

    return collected


def consume_with_default(items: Iterable[Any]) -> list[Any]:
    # 用一個專用的 sentinel 來代表「真的走完了」。
    iterator = iter(items)
    collected: list[Any] = []
    sentinel = object()

    while True:
        item = next(iterator, sentinel)
        if item is sentinel:
            break
        collected.append(item)

    return collected


class CountDown:
    # 可迭代物件要提供 __iter__()。
    def __init__(self, start: int) -> None:
        self.start = start

    def __iter__(self) -> "CountDownIterator":
        return CountDownIterator(self.start)


class CountDownIterator:
    # 迭代器除了要有 __next__()，通常也會讓 __iter__() 回傳自己。
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
    # 只要 iter() 不會報錯，就代表它是可迭代物件。
    try:
        iter(value)
    except TypeError:
        return False
    return True


def is_iterator(value: Any) -> bool:
    # 這裡用最直觀的判斷：同時有 __iter__ 和 __next__。
    return hasattr(value, "__iter__") and hasattr(value, "__next__")
