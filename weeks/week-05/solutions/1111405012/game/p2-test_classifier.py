"""Phase 2 分類器測試。

這份測試依照 p2-test.md / p2-dev.md 設計，預期後續會提供：
1. game/models.py
2. game/classifier.py

已處理的規格假設：
1. 兩張同 rank 牌應優先被視為 PAIR，因此 p2-test.md 中
   `test_classify_triple_not_enough` 不採用 `None`，而是驗證「不是 TRIPLE」。
2. p2-test.md 對非單張牌型的 classify 結果，一律將第三欄固定為 0；
   compare 的花色勝負則另外直接用牌組案例驗證。

直接執行：
    python weeks/week-05/solutions/1111405012/game/p2-test_classifier.py
"""

from __future__ import annotations

import importlib
import importlib.util
import sys
import unittest
from pathlib import Path


CURRENT_DIR = Path(__file__).resolve().parent
PACKAGE_ROOT = CURRENT_DIR.parent

# 讓 `game.xxx` 匯入在直接執行測試檔時也能成立。
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))


def load_module(module_name: str, filename: str, missing_message: str):
    """先嘗試匯入 game 套件，再退回同目錄的單檔模組。"""
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


class BaseClassifierTestCase(unittest.TestCase):
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
            "找不到 game.classifier。請先依 p2-dev.md 實作 classifier.py。",
        )

        missing_models = [
            name for name in ("Card",) if not hasattr(cls.models, name)
        ]
        if missing_models:
            raise AssertionError(
                "game.models 缺少必要類別: " + ", ".join(missing_models)
            )

        missing_classifier = [
            name
            for name in ("CardType", "HandClassifier")
            if not hasattr(cls.classifier_module, name)
        ]
        if missing_classifier:
            raise AssertionError(
                "game.classifier 缺少必要類別: " + ", ".join(missing_classifier)
            )

        cls.Card = cls.models.Card
        cls.CardType = cls.classifier_module.CardType
        cls.HandClassifier = cls.classifier_module.HandClassifier

    def card(self, rank: int, suit: int):
        return self.Card(rank, suit)


# 驗證列舉值是否與規格固定，避免後續 compare / can_play 判斷失配。
class TestCardType(BaseClassifierTestCase):
    def test_cardtype_values(self):
        self.assertEqual(self.CardType.SINGLE.value, 1)
        self.assertEqual(self.CardType.PAIR.value, 2)
        self.assertEqual(self.CardType.TRIPLE.value, 3)
        self.assertEqual(self.CardType.STRAIGHT.value, 4)
        self.assertEqual(self.CardType.FLUSH.value, 5)
        self.assertEqual(self.CardType.FULL_HOUSE.value, 6)
        self.assertEqual(self.CardType.FOUR_OF_A_KIND.value, 7)
        self.assertEqual(self.CardType.STRAIGHT_FLUSH.value, 8)


# 單張是最基本的牌型，這組測試先固定 rank / suit 的輸出格式。
class TestSingleClassification(BaseClassifierTestCase):
    def test_classify_single_ace(self):
        result = self.HandClassifier.classify([self.card(14, 3)])
        self.assertEqual(result, (self.CardType.SINGLE, 14, 3))

    def test_classify_single_two(self):
        result = self.HandClassifier.classify([self.card(15, 0)])
        self.assertEqual(result, (self.CardType.SINGLE, 15, 0))

    def test_classify_single_three(self):
        result = self.HandClassifier.classify([self.card(3, 0)])
        self.assertEqual(result, (self.CardType.SINGLE, 3, 0))


# 對子必須同 rank；第三個欄位依規格文件固定為 0。
class TestPairClassification(BaseClassifierTestCase):
    def test_classify_pair(self):
        result = self.HandClassifier.classify([self.card(14, 3), self.card(14, 2)])
        self.assertEqual(result, (self.CardType.PAIR, 14, 0))

    def test_classify_pair_diff_rank(self):
        result = self.HandClassifier.classify([self.card(14, 3), self.card(13, 3)])
        self.assertIsNone(result)

    def test_classify_pair_from_three(self):
        # 用切片模擬從三條裡挑兩張出牌。
        cards = [self.card(14, 3), self.card(14, 2), self.card(14, 1)]
        result = self.HandClassifier.classify(cards[:2])
        self.assertEqual(result, (self.CardType.PAIR, 14, 0))


# 三條與對子的差別只有張數，但這兩類是後續葫蘆判斷的基礎。
class TestTripleClassification(BaseClassifierTestCase):
    def test_classify_triple(self):
        result = self.HandClassifier.classify(
            [self.card(14, 3), self.card(14, 2), self.card(14, 1)]
        )
        self.assertEqual(result, (self.CardType.TRIPLE, 14, 0))

    def test_classify_triple_not_enough(self):
        # 規格文件此處寫成 None，但同一份文件已定義兩張同 rank 為對子。
        result = self.HandClassifier.classify([self.card(14, 3), self.card(14, 2)])
        self.assertIsNotNone(result)
        self.assertNotEqual(result, (self.CardType.TRIPLE, 14, 0))


# 五張牌型是大老二規則核心，這裡依規格文件逐一固定案例。
class TestFiveCardClassification(BaseClassifierTestCase):
    def test_classify_straight(self):
        cards = [
            self.card(3, 0),
            self.card(4, 1),
            self.card(5, 2),
            self.card(6, 3),
            self.card(7, 0),
        ]
        result = self.HandClassifier.classify(cards)
        self.assertEqual(result, (self.CardType.STRAIGHT, 7, 0))

    def test_classify_straight_ace_low(self):
        cards = [
            self.card(14, 0),
            self.card(15, 1),
            self.card(3, 2),
            self.card(4, 3),
            self.card(5, 0),
        ]
        result = self.HandClassifier.classify(cards)
        self.assertEqual(result, (self.CardType.STRAIGHT, 5, 0))

    def test_classify_flush(self):
        cards = [
            self.card(3, 0),
            self.card(5, 0),
            self.card(7, 0),
            self.card(9, 0),
            self.card(11, 0),
        ]
        result = self.HandClassifier.classify(cards)
        self.assertEqual(result, (self.CardType.FLUSH, 11, 0))

    def test_classify_full_house(self):
        cards = [
            self.card(14, 3),
            self.card(14, 2),
            self.card(14, 1),
            self.card(15, 0),
            self.card(15, 1),
        ]
        result = self.HandClassifier.classify(cards)
        self.assertEqual(result, (self.CardType.FULL_HOUSE, 14, 0))

    def test_classify_four_of_a_kind(self):
        cards = [
            self.card(14, 3),
            self.card(14, 2),
            self.card(14, 1),
            self.card(14, 0),
            self.card(3, 1),
        ]
        result = self.HandClassifier.classify(cards)
        self.assertEqual(result, (self.CardType.FOUR_OF_A_KIND, 14, 0))

    def test_classify_straight_flush(self):
        cards = [
            self.card(3, 0),
            self.card(4, 0),
            self.card(5, 0),
            self.card(6, 0),
            self.card(7, 0),
        ]
        result = self.HandClassifier.classify(cards)
        self.assertEqual(result, (self.CardType.STRAIGHT_FLUSH, 7, 0))


# compare 應處理同牌型大小比較，以及不同牌型的階級比較。
class TestCompare(BaseClassifierTestCase):
    def test_compare_single_rank(self):
        result = self.HandClassifier.compare([self.card(14, 3)], [self.card(13, 3)])
        self.assertEqual(result, 1)

    def test_compare_single_suit(self):
        result = self.HandClassifier.compare([self.card(14, 3)], [self.card(14, 2)])
        self.assertEqual(result, 1)

    def test_compare_pair_rank(self):
        play1 = [self.card(14, 3), self.card(14, 2)]
        play2 = [self.card(13, 3), self.card(13, 0)]
        result = self.HandClassifier.compare(play1, play2)
        self.assertEqual(result, 1)

    def test_compare_pair_suit(self):
        # 同數字對子時，應能再用較大的花色決勝負。
        play1 = [self.card(14, 3), self.card(14, 2)]
        play2 = [self.card(14, 1), self.card(14, 0)]
        result = self.HandClassifier.compare(play1, play2)
        self.assertEqual(result, 1)

    def test_compare_different_type(self):
        pair = [self.card(5, 3), self.card(5, 2)]
        single = [self.card(6, 3)]
        result = self.HandClassifier.compare(pair, single)
        self.assertEqual(result, 1)

    def test_compare_flush_vs_straight(self):
        flush = [
            self.card(3, 0),
            self.card(5, 0),
            self.card(7, 0),
            self.card(9, 0),
            self.card(11, 0),
        ]
        straight = [
            self.card(3, 0),
            self.card(4, 1),
            self.card(5, 2),
            self.card(6, 3),
            self.card(7, 0),
        ]
        result = self.HandClassifier.compare(flush, straight)
        self.assertEqual(result, 1)


# can_play 是實際出牌前的守門檢查，應先擋下不合法的出牌。
class TestCanPlay(BaseClassifierTestCase):
    def test_can_play_first_3clubs(self):
        # 第一手必須包含 3♣。
        result = self.HandClassifier.can_play(None, [self.card(3, 0)])
        self.assertTrue(result)

    def test_can_play_first_not_3clubs(self):
        result = self.HandClassifier.can_play(None, [self.card(14, 3)])
        self.assertFalse(result)

    def test_can_play_same_type(self):
        last_play = [self.card(5, 3), self.card(5, 2)]
        cards = [self.card(6, 3), self.card(6, 1)]
        result = self.HandClassifier.can_play(last_play, cards)
        self.assertTrue(result)

    def test_can_play_diff_type(self):
        last_play = [self.card(5, 3), self.card(5, 2)]
        cards = [self.card(6, 3)]
        result = self.HandClassifier.can_play(last_play, cards)
        self.assertFalse(result)

    def test_can_play_not_stronger(self):
        last_play = [self.card(10, 3), self.card(10, 2)]
        cards = [self.card(5, 3), self.card(5, 2)]
        result = self.HandClassifier.can_play(last_play, cards)
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main(verbosity=2)
