"""Phase 4 AI 策略測試。

這份測試依照 p4-test.md / p4-dev.md 設計，預期後續會提供：
1. game/models.py
2. game/classifier.py
3. game/finder.py
4. game/ai.py

已處理的規格假設：
1. p4-test.md 的 `test_score_single` 與 p4-dev.md 的加分規則互相衝突。
   這裡採用 p4-dev.md 的完整公式，並把各種加分拆成獨立測試。
2. `score_play()` 的「剩1張 / 剩≤3張」加分，採用「出牌後手上剩餘張數」計算。
3. p4-dev.md 只定義 `score_play()` 與 `select_best()`，因此完整策略測試
   會透過 `HandFinder.get_all_valid_plays()` 先找合法牌，再交由 AI 選擇。

直接執行：
    python weeks/week-05/solutions/1111405012/game/p4-test_ai.py
"""

from __future__ import annotations

import importlib
import importlib.util
import sys
import unittest
from pathlib import Path


CURRENT_DIR = Path(__file__).resolve().parent
PACKAGE_ROOT = CURRENT_DIR.parent

# 讓直接執行測試檔時仍可正常使用 `game.xxx` 匯入。
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


class BaseAITestCase(unittest.TestCase):
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
            "找不到 game.finder。請先完成 Phase 3 的 finder.py。",
        )
        cls.ai_module = load_module(
            "ai",
            "ai.py",
            "找不到 game.ai。請先依 p4-dev.md 實作 ai.py。",
        )

        for module, names, module_name in (
            (cls.models, ("Card", "Hand"), "game.models"),
            (cls.classifier_module, ("CardType", "HandClassifier"), "game.classifier"),
            (cls.finder_module, ("HandFinder",), "game.finder"),
            (cls.ai_module, ("AIStrategy",), "game.ai"),
        ):
            missing = [name for name in names if not hasattr(module, name)]
            if missing:
                raise AssertionError(f"{module_name} 缺少必要類別: {', '.join(missing)}")

        cls.Card = cls.models.Card
        cls.Hand = cls.models.Hand
        cls.CardType = cls.classifier_module.CardType
        cls.HandClassifier = cls.classifier_module.HandClassifier
        cls.HandFinder = cls.finder_module.HandFinder
        cls.AIStrategy = cls.ai_module.AIStrategy

    def card(self, rank: int, suit: int):
        return self.Card(rank, suit)

    def hand(self, cards):
        return self.Hand(cards)

    def play_repr(self, play):
        return tuple(sorted(repr(card) for card in play))


# 評分函數應把牌型、點數、收尾加分與黑桃加分整合起來。
class TestScorePlay(BaseAITestCase):
    def test_score_single(self):
        # 用非黑桃且不接近空手的情境，隔離基本分數公式。
        hand = self.hand(
            [
                self.card(14, 2),
                self.card(3, 0),
                self.card(4, 1),
                self.card(5, 2),
                self.card(6, 3),
                self.card(7, 0),
            ]
        )
        score = self.AIStrategy.score_play([self.card(14, 2)], hand)
        self.assertEqual(score, 240)

    def test_score_pair_higher(self):
        hand = self.hand(
            [self.card(9, 3), self.card(9, 2), self.card(5, 1), self.card(3, 0), self.card(4, 1)]
        )
        pair_score = self.AIStrategy.score_play(
            [self.card(9, 3), self.card(9, 2)],
            hand,
        )
        single_score = self.AIStrategy.score_play([self.card(9, 3)], hand)
        self.assertGreater(pair_score, single_score)

    def test_score_triple_higher(self):
        hand = self.hand(
            [
                self.card(9, 3),
                self.card(9, 2),
                self.card(9, 1),
                self.card(3, 0),
                self.card(4, 1),
                self.card(5, 2),
            ]
        )
        triple_score = self.AIStrategy.score_play(
            [self.card(9, 3), self.card(9, 2), self.card(9, 1)],
            hand,
        )
        pair_score = self.AIStrategy.score_play(
            [self.card(9, 3), self.card(9, 2)],
            hand,
        )
        self.assertGreater(triple_score, pair_score)

    def test_score_near_empty(self):
        hand = self.hand([self.card(14, 2), self.card(3, 0)])
        score = self.AIStrategy.score_play([self.card(14, 2)], hand)
        self.assertGreater(score, 10000)

    def test_score_low_cards(self):
        hand = self.hand([self.card(6, 1), self.card(7, 2), self.card(9, 3), self.card(3, 0)])
        score = self.AIStrategy.score_play([self.card(6, 1), self.card(7, 2)], hand)
        self.assertGreater(score, 500)

    def test_score_spade_bonus(self):
        hand = self.hand(
            [self.card(14, 3), self.card(3, 0), self.card(4, 1), self.card(5, 2), self.card(6, 0)]
        )
        spade_score = self.AIStrategy.score_play([self.card(14, 3)], hand)
        heart_score = self.AIStrategy.score_play([self.card(14, 2)], hand)
        self.assertEqual(spade_score - heart_score, 5)


# 選擇最佳牌組時，第一回合要守規則，其餘情境則選最高分。
class TestSelectBest(BaseAITestCase):
    def test_select_best(self):
        hand = self.hand([self.card(6, 3), self.card(6, 1), self.card(14, 2), self.card(3, 0)])
        valid_plays = [
            [self.card(14, 2)],
            [self.card(6, 3), self.card(6, 1)],
        ]
        selected = self.AIStrategy.select_best(valid_plays, hand)
        self.assertEqual(self.play_repr(selected), ("♠6", "♦6"))

    def test_select_first_turn(self):
        hand = self.hand([self.card(3, 0), self.card(4, 1), self.card(5, 2), self.card(6, 3), self.card(7, 0)])
        valid_plays = [
            [self.card(3, 0)],
            [self.card(3, 0), self.card(4, 1), self.card(5, 2), self.card(6, 3), self.card(7, 0)],
        ]
        selected = self.AIStrategy.select_best(valid_plays, hand, is_first=True)
        self.assertEqual(self.play_repr(selected), ("♣3",))

    def test_select_empty(self):
        hand = self.hand([self.card(3, 0), self.card(4, 1)])
        selected = self.AIStrategy.select_best([], hand)
        self.assertIsNone(selected)


# 完整策略測試使用 HandFinder 產生合法牌，再交給 AI 做最終決策。
class TestFullAIStrategy(BaseAITestCase):
    def test_ai_always_plays(self):
        hand = self.hand([self.card(4, 0), self.card(6, 1), self.card(15, 3)])
        last_play = [self.card(5, 0)]
        valid_plays = self.HandFinder.get_all_valid_plays(hand, last_play)
        selected = self.AIStrategy.select_best(valid_plays, hand)

        self.assertTrue(valid_plays)
        self.assertIsNotNone(selected)
        self.assertIn(self.play_repr(selected), [self.play_repr(play) for play in valid_plays])

    def test_ai_prefers_high(self):
        hand = self.hand([self.card(6, 1), self.card(14, 2), self.card(15, 3)])
        last_play = [self.card(5, 0)]
        valid_plays = self.HandFinder.get_all_valid_plays(hand, last_play)
        selected = self.AIStrategy.select_best(valid_plays, hand)

        self.assertEqual(self.play_repr(selected), ("♠2",))

    def test_ai_try_empty(self):
        hand = self.hand([self.card(14, 3)])
        valid_plays = [[self.card(14, 3)]]
        selected = self.AIStrategy.select_best(valid_plays, hand)

        self.assertEqual(self.play_repr(selected), ("♠A",))
        self.assertGreater(self.AIStrategy.score_play(selected, hand), 10000)


if __name__ == "__main__":
    unittest.main(verbosity=2)
