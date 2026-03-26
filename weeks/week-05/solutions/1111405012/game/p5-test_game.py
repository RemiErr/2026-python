"""Phase 5 遊戲流程測試。

這份測試依照 p5-test.md / p5-dev.md 設計，預期後續會提供：
1. game/models.py
2. game/classifier.py
3. game/finder.py
4. game/ai.py
5. game/game.py

已處理的規格假設：
1. `last_play` 可能是純牌組，或是 `(牌組, 玩家名稱)`；測試會先抽出牌組再驗證。
2. `check_round_reset()` 被視為「三人過牌後重置回合」的明確入口，因此 round reset
   測試會直接呼叫它，而不強制要求 `pass_()` 內部一定自動重置。
3. `setup()` 會洗牌，因此初始化測試只驗證不變條件，不綁定特定牌序。

直接執行：
    python weeks/week-05/solutions/1111405012/game/p5-test_game.py
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


class BaseGameTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.models = load_module(
            "models",
            "models.py",
            "找不到 game.models。請先完成 Phase 1 的 models.py。",
        )
        cls.game_module = load_module(
            "game",
            "game.py",
            "找不到 game.game。請先依 p5-dev.md 實作 game.py。",
        )

        for module, names, module_name in (
            (cls.models, ("Card", "Deck", "Hand", "Player"), "game.models"),
            (cls.game_module, ("BigTwoGame",), "game.game"),
        ):
            missing = [name for name in names if not hasattr(module, name)]
            if missing:
                raise AssertionError(f"{module_name} 缺少必要類別: {', '.join(missing)}")

        cls.Card = cls.models.Card
        cls.Deck = cls.models.Deck
        cls.Hand = cls.models.Hand
        cls.Player = cls.models.Player
        cls.BigTwoGame = cls.game_module.BigTwoGame

    def card(self, rank: int, suit: int):
        return self.Card(rank, suit)

    def player(self, name: str, is_ai: bool, cards):
        player = self.Player(name, is_ai)
        player.take_cards(cards)
        return player

    def make_manual_game(self):
        """建立一個可控的遊戲狀態，避免每次都依賴 setup() 隨機發牌。"""
        game = self.BigTwoGame()
        player_1 = self.player("Player1", False, [self.card(3, 0), self.card(4, 1)])
        player_2 = self.player("AI_1", True, [self.card(5, 0), self.card(6, 1)])
        player_3 = self.player("AI_2", True, [self.card(7, 0), self.card(8, 1)])
        player_4 = self.player("AI_3", True, [self.card(9, 0), self.card(10, 1)])

        game.deck = self.Deck()
        game.players = [player_1, player_2, player_3, player_4]
        game.current_player = 0
        game.last_play = None
        game.pass_count = 0
        game.winner = None
        game.round_number = 1
        return game

    def extract_last_play_cards(self, last_play):
        """兼容 `last_play` 的兩種可能格式。"""
        if last_play is None:
            return None
        if isinstance(last_play, tuple):
            return last_play[0]
        return last_play

    def play_repr(self, cards):
        return tuple(sorted(repr(card) for card in cards))


# 初始化測試主要驗證 setup() 是否正確建立 4 人局與完整發牌。
class TestGameSetup(BaseGameTestCase):
    def test_game_has_4_players(self):
        game = self.BigTwoGame()
        game.setup()
        self.assertEqual(len(game.players), 4)

    def test_each_player_13_cards(self):
        game = self.BigTwoGame()
        game.setup()
        self.assertTrue(all(len(player.hand) == 13 for player in game.players))

    def test_total_cards_distributed(self):
        game = self.BigTwoGame()
        game.setup()
        total_cards = sum(len(player.hand) for player in game.players)
        self.assertEqual(total_cards, 52)

    def test_first_player_has_3_clubs(self):
        game = self.BigTwoGame()
        game.setup()
        first_player = game.players[game.current_player]
        self.assertIsNotNone(first_player.hand.find_3_clubs())

    def test_one_human_three_ai(self):
        game = self.BigTwoGame()
        game.setup()
        ai_count = sum(1 for player in game.players if player.is_ai)
        human_count = sum(1 for player in game.players if not player.is_ai)
        self.assertEqual(ai_count, 3)
        self.assertEqual(human_count, 1)


# 出牌流程測試關注合法性判斷與狀態更新，不強綁回合切換細節。
class TestPlayFlow(BaseGameTestCase):
    def test_play_removes_cards(self):
        game = self.make_manual_game()
        player = game.players[0]
        original_count = len(player.hand)

        result = game.play(player, [self.card(3, 0)])

        self.assertTrue(result)
        self.assertEqual(len(player.hand), original_count - 1)

    def test_play_sets_last_play(self):
        game = self.make_manual_game()
        player = game.players[0]

        result = game.play(player, [self.card(3, 0)])
        last_play_cards = self.extract_last_play_cards(game.last_play)

        self.assertTrue(result)
        self.assertIsNotNone(last_play_cards)
        self.assertEqual(self.play_repr(last_play_cards), ("♣3",))

    def test_invalid_play(self):
        game = self.make_manual_game()
        player = game.players[0]
        game.last_play = [self.card(5, 0)]
        original_hand = list(player.hand)

        result = game.play(player, [self.card(4, 1)])

        self.assertFalse(result)
        self.assertEqual(self.play_repr(player.hand), self.play_repr(original_hand))

    def test_pass_increments(self):
        game = self.make_manual_game()
        player = game.players[1]
        game.current_player = 1
        game.last_play = [self.card(3, 0)]

        result = game.pass_(player)

        self.assertTrue(result)
        self.assertEqual(game.pass_count, 1)

    def test_play_advances_turn(self):
        game = self.make_manual_game()
        player = game.players[0]

        result = game.play(player, [self.card(3, 0)])

        self.assertTrue(result)
        self.assertEqual(game.current_player, 1)

    def test_new_round_can_lead_without_3_clubs(self):
        game = self.make_manual_game()
        player = game.players[1]
        game.current_player = 1
        game.last_play = None
        game.opening_required = False

        result = game.play(player, [self.card(5, 0)])

        self.assertTrue(result)


# 回合判定測試單獨驗證 reset 與輪轉邏輯，避免把多個責任混在一起。
class TestTurnLogic(BaseGameTestCase):
    def test_three_passes_resets(self):
        game = self.make_manual_game()
        game.last_play = [self.card(5, 0)]
        game.pass_count = 3

        game.check_round_reset()

        self.assertIsNone(game.last_play)

    def test_turn_rotates(self):
        game = self.make_manual_game()
        game.current_player = 3

        game.next_turn()

        self.assertEqual(game.current_player, 0)


# 獲勝判定只關心手牌是否清空，以及遊戲是否被標記為結束。
class TestWinnerLogic(BaseGameTestCase):
    def test_detect_winner(self):
        game = self.make_manual_game()
        winner = game.players[0]
        winner.hand = self.Hand()

        result = game.check_winner()

        self.assertIs(result, winner)

    def test_no_winner_yet(self):
        game = self.make_manual_game()
        result = game.check_winner()
        self.assertIsNone(result)

    def test_game_ends(self):
        game = self.make_manual_game()
        winner = game.players[0]
        winner.hand = self.Hand()

        game.check_winner()

        self.assertTrue(game.is_game_over())


if __name__ == "__main__":
    unittest.main(verbosity=2)
