from __future__ import annotations

from collections import Counter
from enum import Enum

try:
    from .models import Card
except ImportError:
    from models import Card


class CardType(Enum):
    SINGLE = 1
    PAIR = 2
    TRIPLE = 3
    STRAIGHT = 4
    FLUSH = 5
    FULL_HOUSE = 6
    FOUR_OF_A_KIND = 7
    STRAIGHT_FLUSH = 8


class HandClassifier:
    @staticmethod
    def _is_straight(ranks: list[int]) -> bool:
        return HandClassifier._straight_high_rank(ranks) is not None

    @staticmethod
    def _is_flush(suits: list[int]) -> bool:
        return len(set(suits)) == 1

    @staticmethod
    def _straight_high_rank(ranks: list[int]) -> int | None:
        """回傳順子的最大 rank；A-2-3-4-5 視為 5 高順。"""
        unique_ranks = sorted(set(ranks))
        if len(unique_ranks) != 5:
            return None

        if unique_ranks == [3, 4, 5, 14, 15]:
            return 5

        if all(
            unique_ranks[index] + 1 == unique_ranks[index + 1]
            for index in range(4)
        ):
            return unique_ranks[-1]

        return None

    @staticmethod
    def _highest_suit_for_rank(cards: list[Card], rank: int) -> int:
        return max(card.suit for card in cards if card.rank == rank)

    @staticmethod
    def _rank_counter(cards: list[Card]) -> Counter[int]:
        return Counter(card.rank for card in cards)

    @staticmethod
    def classify(cards: list[Card]) -> tuple[CardType, int, int] | None:
        card_count = len(cards)
        if card_count == 0:
            return None

        ranks = [card.rank for card in cards]
        suits = [card.suit for card in cards]
        rank_counts = HandClassifier._rank_counter(cards)

        if card_count == 1:
            card = cards[0]
            return (CardType.SINGLE, card.rank, card.suit)

        if card_count == 2 and len(rank_counts) == 1:
            return (CardType.PAIR, ranks[0], 0)

        if card_count == 3 and len(rank_counts) == 1:
            return (CardType.TRIPLE, ranks[0], 0)

        if card_count != 5:
            return None

        straight_high = HandClassifier._straight_high_rank(ranks)
        is_flush = HandClassifier._is_flush(suits)

        if straight_high is not None and is_flush:
            return (CardType.STRAIGHT_FLUSH, straight_high, 0)

        if 4 in rank_counts.values():
            four_rank = max(rank for rank, count in rank_counts.items() if count == 4)
            return (CardType.FOUR_OF_A_KIND, four_rank, 0)

        if sorted(rank_counts.values()) == [2, 3]:
            triple_rank = max(rank for rank, count in rank_counts.items() if count == 3)
            return (CardType.FULL_HOUSE, triple_rank, 0)

        if is_flush:
            return (CardType.FLUSH, max(ranks), 0)

        if straight_high is not None:
            return (CardType.STRAIGHT, straight_high, 0)

        return None

    @staticmethod
    def _comparison_key(cards: list[Card]):
        classified = HandClassifier.classify(cards)
        if classified is None:
            return None

        card_type, rank_value, suit_value = classified
        if card_type == CardType.SINGLE:
            return (card_type.value, rank_value, suit_value)

        if card_type == CardType.PAIR:
            return (
                card_type.value,
                rank_value,
                max(card.suit for card in cards),
            )

        if card_type == CardType.TRIPLE:
            return (card_type.value, rank_value)

        if card_type in (CardType.STRAIGHT, CardType.STRAIGHT_FLUSH):
            high_suit = HandClassifier._highest_suit_for_rank(cards, rank_value)
            return (card_type.value, rank_value, high_suit)

        if card_type == CardType.FLUSH:
            sorted_cards = tuple(
                sorted([(card.rank, card.suit) for card in cards], reverse=True)
            )
            return (card_type.value, sorted_cards)

        if card_type == CardType.FULL_HOUSE:
            counts = HandClassifier._rank_counter(cards)
            pair_rank = max(rank for rank, count in counts.items() if count == 2)
            return (card_type.value, rank_value, pair_rank)

        if card_type == CardType.FOUR_OF_A_KIND:
            counts = HandClassifier._rank_counter(cards)
            kicker_rank = max(rank for rank, count in counts.items() if count == 1)
            return (card_type.value, rank_value, kicker_rank)

        return (card_type.value, rank_value)

    @staticmethod
    def compare(play1: list[Card], play2: list[Card]) -> int:
        key1 = HandClassifier._comparison_key(play1)
        key2 = HandClassifier._comparison_key(play2)

        if key1 is None and key2 is None:
            return 0
        if key1 is None:
            return -1
        if key2 is None:
            return 1
        if key1 > key2:
            return 1
        if key1 < key2:
            return -1
        return 0

    @staticmethod
    def can_play(last_play: list[Card] | None, cards: list[Card]) -> bool:
        current = HandClassifier.classify(cards)
        if current is None:
            return False

        if last_play is None:
            # 第一手只允許包含 3♣ 的合法牌型。
            return any(card.rank == 3 and card.suit == 0 for card in cards)

        previous = HandClassifier.classify(last_play)
        if previous is None:
            return False

        if len(cards) != len(last_play):
            return False

        # 單張 / 對子 / 三條需同牌型，五張牌則允許用更高牌型壓制。
        if len(cards) in (1, 2, 3) and current[0] != previous[0]:
            return False

        return HandClassifier.compare(cards, last_play) > 0
