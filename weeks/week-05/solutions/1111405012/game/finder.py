from __future__ import annotations

from itertools import combinations

try:
    from .classifier import HandClassifier
    from .models import Card, Hand
except ImportError:
    from classifier import HandClassifier
    from models import Card, Hand


class HandFinder:
    @staticmethod
    def find_singles(hand: Hand) -> list[list[Card]]:
        return [[card] for card in hand]

    @staticmethod
    def find_pairs(hand: Hand) -> list[list[Card]]:
        pairs: list[list[Card]] = []
        for combo in combinations(hand, 2):
            if combo[0].rank == combo[1].rank:
                pairs.append(list(combo))
        return pairs

    @staticmethod
    def find_triples(hand: Hand) -> list[list[Card]]:
        triples: list[list[Card]] = []
        for combo in combinations(hand, 3):
            if len({card.rank for card in combo}) == 1:
                triples.append(list(combo))
        return triples

    @staticmethod
    def _find_straight_from(hand: Hand, start_rank: int) -> list[Card] | None:
        ranks = [start_rank + offset for offset in range(5)]
        if ranks == [14, 15, 16, 17, 18]:
            return None

        if start_rank == 14:
            ranks = [14, 15, 3, 4, 5]

        straight_cards: list[Card] = []
        for rank in ranks:
            choices = [card for card in hand if card.rank == rank]
            if not choices:
                return None
            straight_cards.append(max(choices, key=lambda card: card.suit))
        return straight_cards

    @staticmethod
    def find_fives(hand: Hand) -> list[list[Card]]:
        plays: list[list[Card]] = []
        seen: set[tuple[tuple[int, int], ...]] = set()

        for combo in combinations(hand, 5):
            cards = list(combo)
            classified = HandClassifier.classify(cards)
            if classified is None:
                continue
            if classified[0].value < 4:
                continue

            key = tuple(sorted((card.rank, card.suit) for card in cards))
            if key in seen:
                continue
            seen.add(key)
            plays.append(cards)

        return plays

    @staticmethod
    def _all_opening_plays(hand: Hand) -> list[list[Card]]:
        return (
            HandFinder.find_singles(hand)
            + HandFinder.find_pairs(hand)
            + HandFinder.find_triples(hand)
            + HandFinder.find_fives(hand)
        )

    @staticmethod
    def get_all_valid_plays(
        hand: Hand,
        last_play: list[Card] | None,
        require_three_clubs: bool | None = None,
    ) -> list[list[Card]]:
        if last_play is None:
            if require_three_clubs is None:
                require_three_clubs = True

            if require_three_clubs:
                three_clubs = [
                    card for card in hand if card.rank == 3 and card.suit == 0
                ]
                return [[three_clubs[0]]] if three_clubs else []

            return HandFinder._all_opening_plays(hand)

        size = len(last_play)
        if size == 1:
            candidates = HandFinder.find_singles(hand)
        elif size == 2:
            candidates = HandFinder.find_pairs(hand)
        elif size == 3:
            candidates = HandFinder.find_triples(hand)
        elif size == 5:
            candidates = HandFinder.find_fives(hand)
        else:
            return []

        return [
            play for play in candidates if HandClassifier.can_play(last_play, list(play))
        ]
