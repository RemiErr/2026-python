from __future__ import annotations

import pygame


class InputHandler:
    def __init__(self, renderer, buttons=None, message_sink=None):
        self.renderer = renderer
        self.selected_indices: list[int] = []
        self.buttons = buttons or {}
        self.message_sink = message_sink
        self.last_message = ""

    def _set_message(self, message: str) -> None:
        self.last_message = message
        if callable(self.message_sink):
            self.message_sink(message)

    def handle_event(self, event, game) -> bool:
        if event.type == pygame.MOUSEBUTTONDOWN:
            return self.handle_click(event.pos, game)
        if event.type == pygame.KEYDOWN:
            return self.handle_key(event.key, game)
        return False

    def _button_rect(self, button):
        return getattr(button, "rect", None) or button.get("rect")

    def _button_action(self, button):
        return getattr(button, "action", None) or button.get("action")

    def handle_click(self, pos, game) -> bool:
        for button in self.buttons.values():
            rect = self._button_rect(button)
            if rect and rect.collidepoint(pos):
                action = self._button_action(button)
                if action == "play":
                    return self.try_play(game)
                if action == "pass":
                    current_player = game.get_current_player()
                    passed = game.pass_(current_player)
                    self._set_message(getattr(game, "last_action_message", ""))
                    return passed

        player = game.get_current_player()
        if player.is_ai or not player.hand:
            if player.is_ai:
                self._set_message("目前是 AI 回合。")
            return False

        screen_height = self.renderer.screen.get_height()
        hand_x = 20
        hand_y = screen_height - self.renderer.CARD_HEIGHT - 20
        hand_width = self.renderer.CARD_WIDTH + max(
            0,
            len(player.hand) - 1,
        ) * getattr(self.renderer, "CARD_GAP", self.renderer.CARD_WIDTH)
        if pos[1] < hand_y or pos[1] > screen_height:
            return False
        if pos[0] < hand_x or pos[0] > hand_x + hand_width:
            return False

        index = min(
            len(player.hand) - 1,
            max(
                0,
                (pos[0] - hand_x)
                // max(1, getattr(self.renderer, "CARD_GAP", self.renderer.CARD_WIDTH)),
            ),
        )
        if index in self.selected_indices:
            self.selected_indices.remove(index)
        else:
            self.selected_indices.append(index)
        self.selected_indices.sort()
        self._set_message(f"已選擇 {len(self.selected_indices)} 張牌。")
        return True

    def handle_key(self, key, game) -> bool:
        if key == pygame.K_RETURN:
            return self.try_play(game)
        if key == pygame.K_p:
            current_player = game.get_current_player()
            return game.pass_(current_player)
        return False

    def try_play(self, game) -> bool:
        current_player = game.get_current_player()
        if current_player.is_ai:
            self._set_message("目前是 AI 回合。")
            return False

        if not self.selected_indices:
            self._set_message("請先選擇要出的牌。")
            return False

        cards = [current_player.hand[index] for index in self.selected_indices]
        played = game.play(current_player, cards)
        if played:
            self.selected_indices.clear()
        self._set_message(getattr(game, "last_action_message", ""))
        return played
