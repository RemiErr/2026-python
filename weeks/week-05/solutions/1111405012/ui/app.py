from __future__ import annotations

import sys
from pathlib import Path

import pygame

if __package__ in (None, ""):
    PACKAGE_ROOT = Path(__file__).resolve().parent.parent
    if str(PACKAGE_ROOT) not in sys.path:
        sys.path.insert(0, str(PACKAGE_ROOT))

    from game.game import BigTwoGame
    from ui.input import InputHandler
    from ui.render import Renderer
else:
    from game.game import BigTwoGame
    from .input import InputHandler
    from .render import Renderer


class BigTwoApp:
    def __init__(self):
        pygame.init()
        pygame.font.init()

        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Big Two")
        self.clock = pygame.time.Clock()

        self.renderer = Renderer(self.screen)
        self.buttons = {
            "play": {
                "rect": pygame.Rect(620, 500, 120, 45),
                "label": "Play",
                "action": "play",
            },
            "pass": {
                "rect": pygame.Rect(620, 550, 120, 45),
                "label": "Pass",
                "action": "pass",
            },
        }
        self.status_message = ""
        self.input_handler = InputHandler(
            self.renderer,
            self.buttons,
            self.set_status,
        )
        self.game = BigTwoGame()
        self.game.setup()
        self.set_status(self.game.last_action_message)

    def set_status(self, message):
        self.status_message = message or ""

    def handle_events(self):
        if self.game.is_game_over():
            return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise SystemExit
            self.input_handler.handle_event(event, self.game)

    def process_ai_turns(self):
        while (
            not self.game.is_game_over()
            and self.game.players
            and self.game.get_current_player().is_ai
        ):
            moved = self.game.ai_turn()
            self.set_status(self.game.last_action_message)
            if not moved:
                break

    def render(self):
        self.screen.fill(self.renderer.COLORS["background"])

        if self.game.players:
            for index, player in enumerate(self.game.players):
                if index == 0:
                    self.renderer.draw_player(
                        player,
                        20,
                        520,
                        index == self.game.current_player,
                    )
                else:
                    self.renderer.draw_player(
                        player,
                        20,
                        20 + (index - 1) * 28,
                        index == self.game.current_player,
                    )

            human_player = self.game.players[0]
            self.renderer.draw_hand(
                human_player.hand,
                20,
                600 - self.renderer.CARD_HEIGHT - 20,
                self.input_handler.selected_indices,
            )

        last_play = self.game.last_play
        if isinstance(last_play, tuple):
            cards, player_name = last_play
        else:
            cards = last_play or []
            player_name = ""
        self.renderer.draw_last_play(cards, player_name, 220, 220)
        self.renderer.draw_status(self.status_message, 220, 190)
        self.renderer.draw_buttons(self.buttons)

        if self.game.is_game_over():
            winner = self.game.winner.name if self.game.winner else "Unknown"
            label = self.renderer.font.render(
                f"Winner: {winner}",
                True,
                self.renderer.COLORS["selected"],
            )
            self.screen.blit(label, (260, 120))

        return self.screen

    def run(self):
        while True:
            self.handle_events()
            self.process_ai_turns()
            self.render()
            pygame.display.flip()
            self.clock.tick(30)


if __name__ == "__main__":
    app = BigTwoApp()
    app.run()
