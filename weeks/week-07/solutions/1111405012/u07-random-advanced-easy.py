from __future__ import annotations

import random
import secrets


def repeatable_random_sequence(
    seed: int,
    count: int = 5,
    low: int = 1,
    high: int = 100,
) -> list[int]:
    # 想重現結果，就自己建一個有種子的 Random。
    rng = random.Random(seed)
    return [rng.randint(low, high) for _ in range(count)]


def independent_random_values(seed_a: int, seed_b: int) -> tuple[float, float]:
    return random.Random(seed_a).random(), random.Random(seed_b).random()


def secure_number(limit: int) -> int:
    return secrets.randbelow(limit)


def secure_hex_token(size: int = 16) -> str:
    return secrets.token_hex(size)


def secure_bytes_token(size: int = 16) -> bytes:
    return secrets.token_bytes(size)
