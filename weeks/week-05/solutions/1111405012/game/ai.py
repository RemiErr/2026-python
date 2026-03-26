from __future__ import annotations

try:
    from .classifier import CardType, HandClassifier
    from .models import Card, Hand
except ImportError:
    from classifier import CardType, HandClassifier
    from models import Card, Hand


class AIStrategy:
    TYPE_SCORES = {
        CardType.SINGLE: 1,
        CardType.PAIR: 2,
        CardType.TRIPLE: 3,
        CardType.STRAIGHT: 4,
        CardType.FLUSH: 5,
        CardType.FULL_HOUSE: 6,
        CardType.FOUR_OF_A_KIND: 7,
        CardType.STRAIGHT_FLUSH: 8,
    }

    EMPTY_HAND_BONUS = 10000
    NEAR_EMPTY_BONUS = 500
    SPADE_BONUS = 5

    @staticmethod
    def score_play(cards: list[Card], hand: Hand, is_first: bool = False) -> float:
        classified = HandClassifier.classify(cards)

        if classified is None:
            type_score = max(1, len(cards))
            rank_score = max((card.rank for card in cards), default=0)
        else:
            type_score = AIStrategy.TYPE_SCORES[classified[0]]
            rank_score = classified[1]

        score = type_score * 100 + rank_score * 10

        remaining_cards = len(hand) - len(cards)
        if remaining_cards <= 1:
            score += AIStrategy.EMPTY_HAND_BONUS
        elif remaining_cards <= 3:
            score += AIStrategy.NEAR_EMPTY_BONUS

        score += sum(
            AIStrategy.SPADE_BONUS for card in cards if card.suit == 3
        )

        if is_first and any(card.rank == 3 and card.suit == 0 for card in cards):
            score += 1

        return score

    @staticmethod
    def select_best(
        valid_plays: list[list[Card]],
        hand: Hand,
        is_first: bool = False,
    ) -> list[Card] | None:
        if not valid_plays:
            return None

        if is_first:
            first_turn_plays = [
                play
                for play in valid_plays
                if len(play) == 1 and play[0].rank == 3 and play[0].suit == 0
            ]
            if first_turn_plays:
                return first_turn_plays[0]
            return None

        return max(
            valid_plays,
            key=lambda play: AIStrategy.score_play(play, hand, is_first=is_first),
        )
