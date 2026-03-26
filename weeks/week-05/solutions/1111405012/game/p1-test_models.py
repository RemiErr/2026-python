"""Phase 1 model tests for the Big Two practice project.

Resolved assumptions from the design notes:
1. Card ranks must span 3..15, where 15 represents 2, otherwise Deck cannot
   contain 52 cards.
2. Hand.sort_desc() should follow the example order in p1-test.md:
   sort by rank descending, then suit descending.

Run this file directly:
    python weeks/week-05/solutions/1111405012/game/p1-test_models.py

The loader first tries game.models, then falls back to models.py beside this file.
"""

from __future__ import annotations

import importlib
import importlib.util
import random
import unittest
from pathlib import Path


def load_models_module():
    try:
        return importlib.import_module("game.models")
    except ModuleNotFoundError as exc:
        local_models = Path(__file__).with_name("models.py")
        if not local_models.exists():
            raise AssertionError(
                "找不到 game.models。請先依 p1-dev.md 實作 game/models.py，"
                "或在這個測試檔旁邊提供 models.py。"
            ) from exc

        spec = importlib.util.spec_from_file_location("local_models", local_models)
        if spec is None or spec.loader is None:
            raise AssertionError(f"無法載入本地 models.py: {local_models}")

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module


class BaseModelsTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.models = load_models_module()

        required_names = ("Card", "Deck", "Hand", "Player")
        missing = [name for name in required_names if not hasattr(cls.models, name)]
        if missing:
            raise AssertionError(
                "game.models 缺少必要類別: " + ", ".join(missing)
            )

        cls.Card = cls.models.Card
        cls.Deck = cls.models.Deck
        cls.Hand = cls.models.Hand
        cls.Player = cls.models.Player

    def card(self, rank: int, suit: int):
        return self.Card(rank, suit)


class TestCard(BaseModelsTestCase):
    def test_card_creation(self):
        card = self.Card(rank=14, suit=3)
        self.assertEqual(card.rank, 14)
        self.assertEqual(card.suit, 3)

    def test_card_repr_ace(self):
        self.assertEqual(repr(self.card(14, 3)), "♠A")

    def test_card_repr_three(self):
        self.assertEqual(repr(self.card(3, 0)), "♣3")

    def test_card_compare_suit(self):
        self.assertTrue(self.card(14, 3) > self.card(14, 2))

    def test_card_compare_suit_2(self):
        self.assertTrue(self.card(14, 2) > self.card(14, 1))

    def test_card_compare_suit_3(self):
        self.assertTrue(self.card(14, 1) > self.card(14, 0))

    def test_card_compare_rank_2(self):
        self.assertTrue(self.card(15, 0) > self.card(14, 3))

    def test_card_compare_rank_a(self):
        self.assertTrue(self.card(14, 0) > self.card(13, 3))

    def test_card_compare_equal(self):
        self.assertFalse(self.card(14, 3) > self.card(14, 3))

    def test_card_sort_key(self):
        self.assertEqual(self.card(14, 3).to_sort_key(), (14, 3))


class TestDeck(BaseModelsTestCase):
    def test_deck_has_52_cards(self):
        deck = self.Deck()
        self.assertEqual(len(deck.cards), 52)

    def test_deck_all_unique(self):
        deck = self.Deck()
        self.assertEqual(len(set(deck.cards)), 52)

    def test_deck_all_ranks(self):
        deck = self.Deck()
        ranks = {card.rank for card in deck.cards}
        self.assertEqual(ranks, set(range(3, 16)))

    def test_deck_all_suits(self):
        deck = self.Deck()
        suits = {card.suit for card in deck.cards}
        self.assertEqual(suits, {0, 1, 2, 3})

    def test_deck_shuffle(self):
        deck = self.Deck()
        before = list(deck.cards)
        random.seed(20260326)
        deck.shuffle()
        self.assertNotEqual(deck.cards, before)
        self.assertEqual(len(deck.cards), 52)

    def test_deal_5_cards(self):
        deck = self.Deck()
        dealt = deck.deal(5)
        self.assertEqual(len(dealt), 5)
        self.assertEqual(len(deck.cards), 47)

    def test_deal_multiple(self):
        deck = self.Deck()
        first = deck.deal(5)
        second = deck.deal(3)
        self.assertEqual(len(first), 5)
        self.assertEqual(len(second), 3)
        self.assertEqual(len(deck.cards), 44)

    def test_deal_exceed(self):
        deck = self.Deck()
        dealt = deck.deal(60)
        self.assertEqual(len(dealt), 52)
        self.assertEqual(len(deck.cards), 0)


class TestHand(BaseModelsTestCase):
    def test_hand_creation(self):
        hand = self.Hand([self.card(3, 0), self.card(14, 3), self.card(13, 2)])
        self.assertEqual(len(hand), 3)

    def test_hand_sort_desc(self):
        hand = self.Hand(
            [self.card(3, 0), self.card(14, 3), self.card(3, 3), self.card(13, 2)]
        )
        hand.sort_desc()
        self.assertEqual([repr(card) for card in hand], ["♠A", "♥K", "♠3", "♣3"])

    def test_hand_find_3_clubs(self):
        hand = self.Hand([self.card(14, 3), self.card(3, 0), self.card(3, 1)])
        self.assertEqual(repr(hand.find_3_clubs()), "♣3")

    def test_hand_find_3_clubs_none(self):
        hand = self.Hand([self.card(14, 3), self.card(3, 1)])
        self.assertIsNone(hand.find_3_clubs())

    def test_hand_remove(self):
        ace_spades = self.card(14, 3)
        three_clubs = self.card(3, 0)
        hand = self.Hand([ace_spades, three_clubs])
        hand.remove([three_clubs])
        self.assertEqual(len(hand), 1)
        self.assertEqual(repr(hand[0]), "♠A")

    def test_hand_remove_not_found(self):
        hand = self.Hand([self.card(14, 3), self.card(3, 0)])
        hand.remove([self.card(5, 1)])
        self.assertEqual(len(hand), 2)

    def test_hand_iteration(self):
        hand = self.Hand([self.card(14, 3), self.card(13, 2)])
        self.assertEqual(len(list(hand)), 2)


class TestPlayer(BaseModelsTestCase):
    def test_player_human(self):
        player = self.Player("Player1", False)
        self.assertFalse(player.is_ai)

    def test_player_ai(self):
        player = self.Player("AI_1", True)
        self.assertTrue(player.is_ai)

    def test_player_take(self):
        player = self.Player("Player1")
        player.take_cards([self.card(14, 3), self.card(3, 0)])
        self.assertEqual(len(player.hand), 2)

    def test_player_play(self):
        player = self.Player("Player1")
        ace_spades = self.card(14, 3)
        three_clubs = self.card(3, 0)
        player.take_cards([ace_spades, three_clubs])

        played = player.play_cards([three_clubs])

        self.assertEqual([repr(card) for card in played], ["♣3"])
        self.assertEqual(len(player.hand), 1)
        self.assertEqual(repr(player.hand[0]), "♠A")


if __name__ == "__main__":
    unittest.main(verbosity=2)
