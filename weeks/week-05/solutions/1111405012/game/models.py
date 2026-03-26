from __future__ import annotations

from functools import total_ordering
import random
from typing import Iterable


@total_ordering
class Card:
    SUIT_SYMBOLS = {0: "♣", 1: "♦", 2: "♥", 3: "♠"}
    RANK_SYMBOLS = {
        3: "3",
        4: "4",
        5: "5",
        6: "6",
        7: "7",
        8: "8",
        9: "9",
        10: "T",
        11: "J",
        12: "Q",
        13: "K",
        14: "A",
        15: "2",
    }

    def __init__(self, rank: int, suit: int) -> None:
        self.rank = rank
        self.suit = suit

    def __repr__(self) -> str:
        return f"{self.SUIT_SYMBOLS[self.suit]}{self.RANK_SYMBOLS[self.rank]}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Card):
            return NotImplemented
        return self.to_sort_key() == other.to_sort_key()

    def __hash__(self) -> int:
        return hash(self.to_sort_key())

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Card):
            return NotImplemented
        return self.to_sort_key() < other.to_sort_key()

    def to_sort_key(self) -> tuple[int, int]:
        return (self.rank, self.suit)


class Deck:
    def __init__(self) -> None:
        self.cards = self._create_cards()

    def _create_cards(self) -> list[Card]:
        return [Card(rank, suit) for rank in range(3, 16) for suit in range(4)]

    def shuffle(self) -> None:
        random.shuffle(self.cards)

    def deal(self, n: int) -> list[Card]:
        count = min(n, len(self.cards))
        dealt = self.cards[:count]
        self.cards = self.cards[count:]
        return dealt


class Hand(list[Card]):
    def __init__(self, cards: Iterable[Card] | None = None) -> None:
        super().__init__(cards or [])

    def sort_desc(self) -> None:
        self.sort(key=lambda card: card.to_sort_key(), reverse=True)

    def find_3_clubs(self) -> Card | None:
        for card in self:
            if card.rank == 3 and card.suit == 0:
                return card
        return None

    def remove(self, cards: Iterable[Card]) -> None:  # type: ignore[override]
        for card in cards:
            if card in self:
                super().remove(card)


class Player:
    def __init__(self, name: str, is_ai: bool = False) -> None:
        self.name = name
        self.is_ai = is_ai
        self.hand = Hand()
        self.score = 0

    def take_cards(self, cards: Iterable[Card]) -> None:
        self.hand.extend(cards)

    def play_cards(self, cards: Iterable[Card]) -> list[Card]:
        played_cards = list(cards)
        self.hand.remove(played_cards)
        return played_cards
