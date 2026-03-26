"""Phase 3 牌型搜尋測試。

這份測試依照 p3-test.md / p3-dev.md 設計，預期後續會提供：
1. game/models.py
2. game/classifier.py
3. game/finder.py

已處理的規格假設：
1. `find_fives()` 可能回傳多組候選牌型，因此這裡以「至少包含代表案例」驗證。
2. `get_all_valid_plays()` 的回傳順序未在規格中固定，因此測試採內容驗證，不綁順序。
3. 第一手根據 p3-test.md 採較嚴格規則，只期待回傳單張 `3♣`。

直接執行：
    python weeks/week-05/solutions/1111405012/game/p3-test_finder.py
"""

from __future__ import annotations

import importlib
import importlib.util
import sys
import unittest
from pathlib import Path


CURRENT_DIR = Path(__file__).resolve().parent
PACKAGE_ROOT = CURRENT_DIR.parent

# 讓直接執行測試檔時仍可用 `game.xxx` 匯入。
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))


def load_module(module_name: str, filename: str, missing_message: str):
    """先嘗試匯入 game 套件，再退回同目錄單檔模組。"""
    try:
        return importlib.import_module(f"game.{module_name}")
    except ModuleNotFoundError as exc:
        local_path = CURRENT_DIR / filename
        if not local_path.exists():
            raise AssertionError(missing_message) from exc

        spec = importlib.util.spec_from_file_location(f"local_{module_name}", local_path)
        if spec is None or spec.loader is None:
            raise AssertionError(f"無法載入本地模組：{local_path}")

        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        return module


class BaseFinderTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.models = load_module(
            "models",
            "models.py",
            "找不到 game.models。請先完成 Phase 1 的 models.py。",
        )
        cls.classifier_module = load_module(
            "classifier",
            "classifier.py",
            "找不到 game.classifier。請先完成 Phase 2 的 classifier.py。",
        )
        cls.finder_module = load_module(
            "finder",
            "finder.py",
            "找不到 game.finder。請先依 p3-dev.md 實作 finder.py。",
        )

        for module, names, module_name in (
            (cls.models, ("Card", "Hand"), "game.models"),
            (cls.classifier_module, ("CardType", "HandClassifier"), "game.classifier"),
            (cls.finder_module, ("HandFinder",), "game.finder"),
        ):
            missing = [name for name in names if not hasattr(module, name)]
            if missing:
                raise AssertionError(f"{module_name} 缺少必要類別: {', '.join(missing)}")

        cls.Card = cls.models.Card
        cls.Hand = cls.models.Hand
        cls.CardType = cls.classifier_module.CardType
        cls.HandClassifier = cls.classifier_module.HandClassifier
        cls.HandFinder = cls.finder_module.HandFinder

    def card(self, rank: int, suit: int):
        return self.Card(rank, suit)

    def hand(self, cards):
        return self.Hand(cards)

    def normalize_plays(self, plays):
        """把牌組轉成可比較的 repr tuple，避免被回傳順序影響。"""
        normalized = []
        for play in plays:
            normalized.append(tuple(sorted(repr(card) for card in play)))
        return sorted(normalized)


# 單張搜尋應逐張展開，空手牌則回空清單。
class TestFindSingles(BaseFinderTestCase):
    def test_find_singles(self):
        hand = self.hand([self.card(14, 3), self.card(13, 2), self.card(3, 0)])
        plays = self.HandFinder.find_singles(hand)

        self.assertEqual(len(plays), 3)
        self.assertEqual(
            self.normalize_plays(plays),
            [("♠A",), ("♣3",), ("♥K",)],
        )

    def test_find_singles_empty(self):
        plays = self.HandFinder.find_singles(self.hand([]))
        self.assertEqual(plays, [])


# 對子搜尋重點在同 rank 組合數量，而不是原始牌序。
class TestFindPairs(BaseFinderTestCase):
    def test_find_pairs_one(self):
        hand = self.hand([self.card(14, 3), self.card(14, 2), self.card(3, 0)])
        plays = self.HandFinder.find_pairs(hand)

        self.assertEqual(len(plays), 1)
        self.assertEqual(self.normalize_plays(plays), [("♠A", "♥A")])

    def test_find_pairs_two(self):
        hand = self.hand(
            [self.card(14, 3), self.card(14, 2), self.card(13, 3), self.card(13, 0)]
        )
        plays = self.HandFinder.find_pairs(hand)

        self.assertEqual(len(plays), 2)
        self.assertEqual(
            self.normalize_plays(plays),
            [("♠A", "♥A"), ("♠K", "♣K")],
        )

    def test_find_pairs_none(self):
        hand = self.hand([self.card(14, 3), self.card(13, 2), self.card(3, 0)])
        plays = self.HandFinder.find_pairs(hand)
        self.assertEqual(plays, [])


# 三條搜尋應只取同 rank 的三張組合，其他牌不應干擾結果。
class TestFindTriples(BaseFinderTestCase):
    def test_find_triples_one(self):
        hand = self.hand(
            [self.card(14, 3), self.card(14, 2), self.card(14, 1), self.card(3, 0)]
        )
        plays = self.HandFinder.find_triples(hand)

        self.assertEqual(len(plays), 1)
        self.assertEqual(self.normalize_plays(plays), [("♠A", "♥A", "♦A")])

    def test_find_triples_with_extra(self):
        hand = self.hand(
            [
                self.card(14, 3),
                self.card(14, 2),
                self.card(14, 1),
                self.card(13, 3),
                self.card(13, 0),
            ]
        )
        plays = self.HandFinder.find_triples(hand)

        self.assertEqual(len(plays), 1)
        self.assertEqual(self.normalize_plays(plays), [("♠A", "♥A", "♦A")])


# 五張牌搜尋只驗證必要代表案例存在，避免把所有搜尋策略鎖死。
class TestFindFives(BaseFinderTestCase):
    def test_find_straight(self):
        hand = self.hand(
            [
                self.card(3, 0),
                self.card(4, 1),
                self.card(5, 2),
                self.card(6, 3),
                self.card(7, 0),
                self.card(11, 1),
            ]
        )
        plays = self.HandFinder.find_fives(hand)

        normalized = self.normalize_plays(plays)
        self.assertIn(("♠6", "♣3", "♣7", "♥5", "♦4"), normalized)

    def test_find_flush(self):
        hand = self.hand(
            [
                self.card(3, 0),
                self.card(5, 0),
                self.card(7, 0),
                self.card(9, 0),
                self.card(11, 0),
                self.card(14, 3),
            ]
        )
        plays = self.HandFinder.find_fives(hand)

        normalized = self.normalize_plays(plays)
        self.assertIn(("♣3", "♣5", "♣7", "♣9", "♣J"), normalized)

    def test_find_full_house(self):
        hand = self.hand(
            [
                self.card(14, 3),
                self.card(14, 2),
                self.card(14, 1),
                self.card(15, 0),
                self.card(15, 1),
                self.card(3, 0),
            ]
        )
        plays = self.HandFinder.find_fives(hand)

        normalized = self.normalize_plays(plays)
        self.assertIn(("♠A", "♣2", "♥A", "♦2", "♦A"), normalized)

    def test_find_four_of_a_kind(self):
        hand = self.hand(
            [
                self.card(14, 3),
                self.card(14, 2),
                self.card(14, 1),
                self.card(14, 0),
                self.card(3, 1),
                self.card(5, 0),
            ]
        )
        plays = self.HandFinder.find_fives(hand)

        normalized = self.normalize_plays(plays)
        self.assertIn(("♠A", "♣A", "♥A", "♦3", "♦A"), normalized)

    def test_find_straight_flush(self):
        hand = self.hand(
            [
                self.card(3, 0),
                self.card(4, 0),
                self.card(5, 0),
                self.card(6, 0),
                self.card(7, 0),
                self.card(14, 3),
            ]
        )
        plays = self.HandFinder.find_fives(hand)

        normalized = self.normalize_plays(plays)
        self.assertIn(("♣3", "♣4", "♣5", "♣6", "♣7"), normalized)


# 合法出牌搜尋應同時滿足牌型合法與可壓過上家。
class TestGetAllValidPlays(BaseFinderTestCase):
    def test_first_turn(self):
        hand = self.hand([self.card(3, 0), self.card(14, 3), self.card(13, 2)])
        plays = self.HandFinder.get_all_valid_plays(hand, None)

        self.assertEqual(self.normalize_plays(plays), [("♣3",)])

    def test_with_last_single(self):
        hand = self.hand([self.card(4, 0), self.card(6, 1), self.card(15, 3)])
        last_play = [self.card(5, 0)]
        plays = self.HandFinder.get_all_valid_plays(hand, last_play)

        self.assertTrue(plays)
        self.assertTrue(all(len(play) == 1 for play in plays))
        self.assertTrue(
            all(self.HandClassifier.can_play(last_play, play) for play in plays)
        )
        self.assertEqual(
            self.normalize_plays(plays),
            [("♠2",), ("♦6",)],
        )

    def test_with_last_pair(self):
        hand = self.hand(
            [
                self.card(6, 3),
                self.card(6, 1),
                self.card(7, 2),
                self.card(7, 0),
                self.card(14, 3),
            ]
        )
        last_play = [self.card(5, 3), self.card(5, 2)]
        plays = self.HandFinder.get_all_valid_plays(hand, last_play)

        self.assertTrue(plays)
        self.assertTrue(all(len(play) == 2 for play in plays))
        self.assertTrue(
            all(self.HandClassifier.can_play(last_play, play) for play in plays)
        )
        self.assertEqual(
            self.normalize_plays(plays),
            [("♠6", "♦6"), ("♣7", "♥7")],
        )

    def test_no_valid(self):
        hand = self.hand([self.card(3, 0), self.card(4, 1), self.card(5, 2)])
        last_play = [self.card(15, 3)]
        plays = self.HandFinder.get_all_valid_plays(hand, last_play)
        self.assertEqual(plays, [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
