from __future__ import annotations

import random
import secrets


def repeatable_random_sequence(
    seed: int,
    count: int = 5,
    low: int = 1,
    high: int = 100,
) -> list[int]:
    # 用固定種子建立自己的 Random 物件，結果就能重現。
    rng = random.Random(seed)
    return [rng.randint(low, high) for _ in range(count)]


def independent_random_values(seed_a: int, seed_b: int) -> tuple[float, float]:
    # 不同 Random 實例各有各的亂數流。
    rng_a = random.Random(seed_a)
    rng_b = random.Random(seed_b)
    return rng_a.random(), rng_b.random()


def secure_number(limit: int) -> int:
    # 安全場景請改用 secrets。
    return secrets.randbelow(limit)


def secure_hex_token(size: int = 16) -> str:
    return secrets.token_hex(size)


def secure_bytes_token(size: int = 16) -> bytes:
    return secrets.token_bytes(size)
