"""Phase 6 GUI 測試。

這份測試依照 p6-test.md / p6-dev.md 設計，預期後續會提供：
1. game/models.py
2. game/game.py
3. ui/render.py 或 game/render.py
4. ui/input.py 或 game/input.py
5. ui/app.py 或 game/app.py

已處理的規格假設：
1. p6-test.md 指出 GUI 測試以整合與手動測試為主，因此這裡採「mock pygame + smoke test」
   的方式，避免把實作細節綁太死。
2. `draw_card()` / `draw_hand()` 若直接畫到既有畫布而不回傳 surface，本測試接受用
   renderer 的 screen 作為驗證對象。
3. `handle_click()` 的選牌區域未在規格中明確定義，因此測試會用多組常見座標嘗試驗證
   「點擊手牌區能成功切換選取狀態」。

直接執行：
    python weeks/week-05/solutions/1111405012/game/p6-test_ui.py
"""

from __future__ import annotations

import importlib
import importlib.util
import sys
import types
import unittest
from pathlib import Path
from unittest.mock import MagicMock


CURRENT_DIR = Path(__file__).resolve().parent
PACKAGE_ROOT = CURRENT_DIR.parent

# 讓直接執行測試檔時仍可正常使用 `game.xxx` / `ui.xxx` 匯入。
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))


class FakeSurface:
    def __init__(self, size: tuple[int, int] = (800, 600)):
        self.width, self.height = size
        self.fill_calls = []
        self.blit_calls = []
        self.draw_calls = []

    def get_width(self) -> int:
        return self.width

    def get_height(self) -> int:
        return self.height

    def get_size(self) -> tuple[int, int]:
        return (self.width, self.height)

    def fill(self, color):
        self.fill_calls.append(color)

    def blit(self, surface, pos):
        self.blit_calls.append((surface, pos))
        return FakeRect(pos[0], pos[1], surface.get_width(), surface.get_height())


class FakeRect:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def collidepoint(self, pos: tuple[int, int]) -> bool:
        px, py = pos
        return (
            self.x <= px <= self.x + self.width
            and self.y <= py <= self.y + self.height
        )


class FakeFont:
    def render(self, text: str, antialias: bool, color) -> FakeSurface:
        width = max(10, len(text) * 10)
        return FakeSurface((width, 20))


class FakeClock:
    def tick(self, fps: int) -> int:
        return fps


class ButtonSpec(dict):
    """同時兼容 rect-like 與 dict-like 的按鈕設定。"""

    def __init__(self, x: int, y: int, width: int, height: int, action: str):
        super().__init__()
        self.rect = FakeRect(x, y, width, height)
        self.action = action
        self["rect"] = self.rect
        self["action"] = action

    def collidepoint(self, pos: tuple[int, int]) -> bool:
        return self.rect.collidepoint(pos)


def install_fake_pygame():
    """建立最小可用的 pygame 假模組，隔離 GUI 測試的外部依賴。"""
    pygame_module = types.ModuleType("pygame")
    display_module = types.ModuleType("pygame.display")
    font_module = types.ModuleType("pygame.font")
    draw_module = types.ModuleType("pygame.draw")
    event_module = types.ModuleType("pygame.event")
    time_module = types.ModuleType("pygame.time")

    pygame_module.Surface = FakeSurface
    pygame_module.Rect = FakeRect
    pygame_module.MOUSEBUTTONDOWN = 1
    pygame_module.KEYDOWN = 2
    pygame_module.QUIT = 12
    pygame_module.K_RETURN = 13
    pygame_module.K_p = 80
    pygame_module.init = MagicMock()
    pygame_module.quit = MagicMock()

    display_module.set_mode = MagicMock(side_effect=lambda size: FakeSurface(size))
    display_module.get_surface = MagicMock(side_effect=lambda: FakeSurface((800, 600)))
    display_module.flip = MagicMock()
    display_module.set_caption = MagicMock()

    font_module.init = MagicMock()
    font_module.match_font = MagicMock(return_value=None)
    font_module.SysFont = MagicMock(side_effect=lambda *args, **kwargs: FakeFont())
    font_module.Font = MagicMock(side_effect=lambda *args, **kwargs: FakeFont())

    def draw_rect(surface, color, rect, width=0, border_radius=0):
        fake_rect = rect if isinstance(rect, FakeRect) else FakeRect(*rect)
        surface.draw_calls.append(("rect", color, fake_rect, width, border_radius))
        return fake_rect

    draw_module.rect = MagicMock(side_effect=draw_rect)

    event_module.get = MagicMock(return_value=[])
    event_module.Event = lambda event_type, **kwargs: types.SimpleNamespace(
        type=event_type,
        **kwargs,
    )

    time_module.Clock = FakeClock

    pygame_module.display = display_module
    pygame_module.font = font_module
    pygame_module.draw = draw_module
    pygame_module.event = event_module
    pygame_module.time = time_module

    sys.modules["pygame"] = pygame_module
    sys.modules["pygame.display"] = display_module
    sys.modules["pygame.font"] = font_module
    sys.modules["pygame.draw"] = draw_module
    sys.modules["pygame.event"] = event_module
    sys.modules["pygame.time"] = time_module
    return pygame_module


def load_module(module_name: str, filename: str, missing_message: str):
    """先嘗試匯入 game 套件，再退回同目錄單檔模組。"""
    try:
        return importlib.import_module(f"game.{module_name}")
    except ModuleNotFoundError as exc:
        local_path = CURRENT_DIR / filename
        if not local_path.exists():
            raise AssertionError(missing_message) from exc

        spec = importlib.util.spec_from_file_location(f"game.{module_name}", local_path)
        if spec is None or spec.loader is None:
            raise AssertionError(f"無法載入本地模組：{local_path}")

        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        return module


def load_ui_module(module_name: str, missing_message: str):
    """優先載入 p6-dev.md 指定的 ui 套件，找不到時退回 game 目錄版本。"""
    candidates = [
        (f"ui.{module_name}", PACKAGE_ROOT / "ui" / f"{module_name}.py"),
        (f"game.{module_name}", CURRENT_DIR / f"{module_name}.py"),
    ]

    last_error = None
    for import_name, file_path in candidates:
        try:
            return importlib.import_module(import_name)
        except ModuleNotFoundError as exc:
            last_error = exc
            if not file_path.exists():
                continue

            package_name = import_name.rsplit(".", 1)[0]
            package_dir = file_path.parent
            if package_name not in sys.modules:
                package_module = types.ModuleType(package_name)
                package_module.__path__ = [str(package_dir)]
                sys.modules[package_name] = package_module

            spec = importlib.util.spec_from_file_location(import_name, file_path)
            if spec is None or spec.loader is None:
                raise AssertionError(f"無法載入本地模組：{file_path}")

            module = importlib.util.module_from_spec(spec)
            sys.modules[import_name] = module
            spec.loader.exec_module(module)
            return module

    raise AssertionError(missing_message) from last_error


class BaseUITestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.pygame = install_fake_pygame()

        cls.models = load_module(
            "models",
            "models.py",
            "找不到 game.models。請先完成前面 phase 的 models.py。",
        )
        cls.game_module = load_module(
            "game",
            "game.py",
            "找不到 game.game。請先完成 Phase 5 的 game.py。",
        )
        cls.render_module = load_ui_module(
            "render",
            "找不到 ui.render 或 game/render.py。請先依 p6-dev.md 實作渲染器。",
        )
        cls.input_module = load_ui_module(
            "input",
            "找不到 ui.input 或 game/input.py。請先依 p6-dev.md 實作輸入處理。",
        )
        cls.app_module = load_ui_module(
            "app",
            "找不到 ui.app 或 game/app.py。請先依 p6-dev.md 實作主應用。",
        )

        for module, names, module_name in (
            (cls.models, ("Card", "Hand", "Player"), "game.models"),
            (cls.game_module, ("BigTwoGame",), "game.game"),
            (cls.render_module, ("Renderer",), "ui.render / game.render"),
            (cls.input_module, ("InputHandler",), "ui.input / game.input"),
            (cls.app_module, ("BigTwoApp",), "ui.app / game.app"),
        ):
            missing = [name for name in names if not hasattr(module, name)]
            if missing:
                raise AssertionError(f"{module_name} 缺少必要類別: {', '.join(missing)}")

        cls.Card = cls.models.Card
        cls.Hand = cls.models.Hand
        cls.Player = cls.models.Player
        cls.BigTwoGame = cls.game_module.BigTwoGame
        cls.Renderer = cls.render_module.Renderer
        cls.InputHandler = cls.input_module.InputHandler
        cls.BigTwoApp = cls.app_module.BigTwoApp

    def card(self, rank: int, suit: int):
        return self.Card(rank, suit)

    def hand(self, cards):
        return self.Hand(cards)

    def player(self, name: str, is_ai: bool, cards):
        player = self.Player(name, is_ai)
        player.take_cards(cards)
        return player

    def make_manual_game(self):
        game = self.BigTwoGame()
        game.players = [
            self.player("Player1", False, [self.card(3, 0), self.card(14, 3)]),
            self.player("AI_1", True, [self.card(5, 0)]),
            self.player("AI_2", True, [self.card(6, 1)]),
            self.player("AI_3", True, [self.card(7, 2)]),
        ]
        game.current_player = 0
        game.last_play = None
        game.pass_count = 0
        game.winner = None
        game.round_number = 1
        return game

    def make_renderer(self):
        screen = FakeSurface((800, 600))
        for args in ((screen,), ()):
            try:
                renderer = self.Renderer(*args)
                break
            except TypeError:
                renderer = None
        if renderer is None:
            raise AssertionError("無法建立 Renderer，請檢查 __init__ 介面。")

        if not hasattr(renderer, "screen"):
            renderer.screen = screen
        return renderer, screen

    def make_input_handler(self, renderer):
        for args in ((renderer,), (renderer, {}), ()):
            try:
                handler = self.InputHandler(*args)
                break
            except TypeError:
                handler = None
        if handler is None:
            raise AssertionError("無法建立 InputHandler，請檢查 __init__ 介面。")

        if not hasattr(handler, "renderer"):
            handler.renderer = renderer
        if not hasattr(handler, "selected_indices"):
            handler.selected_indices = []
        if not hasattr(handler, "buttons"):
            handler.buttons = {}
        return handler

    def surface_like(self, result, fallback):
        if hasattr(result, "get_width"):
            return result
        if hasattr(fallback, "screen") and hasattr(fallback.screen, "get_width"):
            return fallback.screen
        if hasattr(fallback, "get_width"):
            return fallback
        raise AssertionError("找不到可驗證的 surface 物件。")

    def play_repr(self, play):
        return tuple(sorted(repr(card) for card in play))


# 渲染測試先驗證最基本的 surface 行為，避免 GUI 一開始就無法畫出內容。
class TestRendering(BaseUITestCase):
    def test_card_color_is_black_for_spades_and_clubs(self):
        renderer, _ = self.make_renderer()
        self.assertEqual(
            renderer._card_color(self.card(14, 3)),
            renderer.COLORS["card_black"],
        )

    def test_card_color_is_red_for_hearts_and_diamonds(self):
        renderer, _ = self.make_renderer()
        self.assertEqual(
            renderer._card_color(self.card(14, 2)),
            renderer.COLORS["card_red"],
        )

    def test_card_render(self):
        renderer, screen = self.make_renderer()
        result = renderer.draw_card(self.card(14, 3), 0, 0)
        surface = self.surface_like(result, renderer if renderer else screen)
        self.assertGreater(surface.get_width(), 0)

    def test_hand_render(self):
        renderer, screen = self.make_renderer()
        result = renderer.draw_hand(
            self.hand([self.card(3, 0), self.card(14, 3), self.card(13, 2)]),
            0,
            0,
            [],
        )
        surface = self.surface_like(result, renderer if renderer else screen)
        self.assertGreater(surface.get_width(), 0)

    def test_status_render(self):
        renderer, screen = self.make_renderer()
        result = renderer.draw_status("test message", 10, 10)
        surface = self.surface_like(result, renderer if renderer else screen)
        self.assertGreater(surface.get_width(), 0)


# 整合測試驗證 GUI 元件是否能正確和遊戲邏輯接起來。
class TestIntegration(BaseUITestCase):
    def test_game_init(self):
        app = self.BigTwoApp()
        self.assertEqual(len(app.game.players), 4)

    def test_card_selection(self):
        app = self.BigTwoApp()
        app.game = self.make_manual_game()
        renderer = getattr(app, "renderer", self.make_renderer()[0])
        handler = getattr(app, "input_handler", self.make_input_handler(renderer))
        handler.buttons = {}
        handler.selected_indices = []

        if hasattr(app, "render"):
            app.render()

        card_width = getattr(renderer, "CARD_WIDTH", 60)
        card_height = getattr(renderer, "CARD_HEIGHT", 90)
        screen = getattr(app, "screen", FakeSurface((800, 600)))
        candidate_positions = [
            (card_width // 2, screen.get_height() - card_height // 2),
            (screen.get_width() // 2, screen.get_height() - card_height // 2),
            (card_width // 2, screen.get_height() - 20),
            (screen.get_width() // 2, screen.get_height() - 20),
        ]

        selected = False
        for pos in candidate_positions:
            handler.selected_indices = []
            try:
                handler.handle_click(pos, app.game)
            except Exception:
                continue
            if handler.selected_indices:
                selected = True
                break

        self.assertTrue(selected)

    def test_button_click(self):
        renderer, _ = self.make_renderer()
        handler = self.make_input_handler(renderer)
        game = self.make_manual_game()
        handler.buttons = {"play": ButtonSpec(0, 0, 120, 50, "play")}
        handler.try_play = MagicMock(return_value=True)

        result = handler.handle_click((10, 10), game)

        self.assertTrue(result)
        handler.try_play.assert_called_once()

    def test_play_without_selection_sets_status(self):
        app = self.BigTwoApp()
        app.game = self.make_manual_game()
        app.input_handler.selected_indices = []

        result = app.input_handler.handle_click((630, 510), app.game)

        self.assertFalse(result)
        self.assertIn("選擇", app.status_message)

    def test_ai_turns_are_processed_until_human(self):
        app = self.BigTwoApp()
        app.game = self.make_manual_game()
        app.game.players[1].hand = self.Hand([self.card(5, 0), self.card(9, 0)])
        app.game.players[2].hand = self.Hand([self.card(6, 1), self.card(10, 1)])
        app.game.players[3].hand = self.Hand([self.card(7, 2), self.card(11, 2)])
        app.game.current_player = 1
        app.game.last_play = [self.card(4, 0)]
        app.game.opening_required = False

        app.process_ai_turns()

        self.assertEqual(app.game.current_player, 0)
        last_play_cards = (
            app.game.last_play[0]
            if isinstance(app.game.last_play, tuple)
            else app.game.last_play
        )
        self.assertEqual(self.play_repr(last_play_cards), ("♥J",))


# E2E 測試以 smoke test 形式驗證：完成一局後 GUI 仍能正確 render。
class TestEndToEnd(BaseUITestCase):
    def test_complete_flow(self):
        app = self.BigTwoApp()
        app.game = self.make_manual_game()
        current_player = app.game.players[0]
        current_player.hand = self.Hand([self.card(3, 0)])

        played = app.game.play(current_player, [self.card(3, 0)])
        if hasattr(app, "render"):
            app.render()

        self.assertTrue(played)
        self.assertTrue(app.game.is_game_over())


if __name__ == "__main__":
    unittest.main(verbosity=2)
