from __future__ import annotations

import pygame


class Renderer:
    UI_FONT_CANDIDATES = [
        "Microsoft JhengHei",
        "Noto Sans CJK TC",
        "Microsoft YaHei",
        "Arial Unicode MS",
    ]
    SYMBOL_FONT_CANDIDATES = [
        "Segoe UI Symbol",
        "Noto Sans Symbols 2",
        "DejaVu Sans",
        "Arial Unicode MS",
    ]

    COLORS = {
        "background": (45, 45, 45),
        "card_face": (245, 245, 245),
        "card_back": (74, 144, 217),
        "text_primary": (20, 20, 20),
        "text_light": (245, 245, 245),
        "card_black": (20, 20, 20),
        "card_red": (220, 70, 55),
        "player": (46, 204, 113),
        "ai": (149, 165, 166),
        "selected": (241, 196, 15),
        "button": (52, 152, 219),
        "status_bg": (248, 226, 143),
        "text_dark": (35, 35, 35),
    }

    CARD_WIDTH = 60
    CARD_HEIGHT = 90
    CARD_GAP = 40

    def __init__(self, screen=None):
        self.screen = screen or pygame.display.get_surface() or pygame.display.set_mode(
            (800, 600)
        )
        self.font = self._load_font(self.UI_FONT_CANDIDATES, 24)
        self.small_font = self._load_font(self.UI_FONT_CANDIDATES, 18)
        self.card_rank_font = self._load_font(self.UI_FONT_CANDIDATES, 24)
        self.card_suit_font = self._load_font(self.SYMBOL_FONT_CANDIDATES, 22)

    def _load_font(self, candidates, size):
        match_font = getattr(pygame.font, "match_font", None)
        if callable(match_font):
            for name in candidates:
                font_path = match_font(name)
                if font_path:
                    return pygame.font.Font(font_path, size)
        if candidates:
            return pygame.font.SysFont(candidates[0], size)
        return pygame.font.SysFont(None, size)

    def _card_rank_text(self, card):
        return card.RANK_SYMBOLS[card.rank]

    def _card_suit_text(self, card):
        return card.SUIT_SYMBOLS[card.suit]

    def _card_color(self, card):
        if card.suit in (1, 2):
            return self.COLORS["card_red"]
        return self.COLORS["card_black"]

    def draw_card(self, card, x, y, selected=False):
        card_surface = pygame.Surface((self.CARD_WIDTH, self.CARD_HEIGHT))
        card_surface.fill(self.COLORS["card_face"])

        border_color = (
            self.COLORS["selected"] if selected else self.COLORS["button"]
        )
        pygame.draw.rect(
            card_surface,
            border_color,
            (0, 0, self.CARD_WIDTH, self.CARD_HEIGHT),
            2,
        )

        text_color = self._card_color(card)
        rank_label = self.card_rank_font.render(
            self._card_rank_text(card),
            True,
            text_color,
        )
        suit_label = self.card_suit_font.render(
            self._card_suit_text(card),
            True,
            text_color,
        )
        card_surface.blit(rank_label, (8, 8))
        card_surface.blit(suit_label, (8, 34))
        self.screen.blit(card_surface, (x, y))
        return card_surface

    def draw_hand(self, hand, x, y, selected_indices):
        for index, card in enumerate(hand):
            card_x = x + index * self.CARD_GAP
            selected = index in selected_indices
            card_y = y - 15 if selected else y
            self.draw_card(card, card_x, card_y, selected=selected)
        return self.screen

    def draw_player(self, player, x, y, is_current):
        color = self.COLORS["player"] if not player.is_ai else self.COLORS["ai"]
        if is_current:
            color = self.COLORS["selected"]

        label = self.font.render(
            f"{player.name} ({len(player.hand)})",
            True,
            color,
        )
        self.screen.blit(label, (x, y))
        return label

    def draw_last_play(self, cards, player_name, x, y):
        if player_name:
            label = self.small_font.render(
                f"Last: {player_name}",
                True,
                self.COLORS["text_light"],
            )
            self.screen.blit(label, (x, y - 24))

        for index, card in enumerate(cards or []):
            self.draw_card(card, x + index * self.CARD_GAP, y)
        return self.screen

    def draw_buttons(self, buttons, x=0, y=0):
        for button in buttons.values():
            rect = getattr(button, "rect", None) or button.get("rect")
            label_text = button.get("label") if isinstance(button, dict) else None
            if label_text is None:
                label_text = getattr(button, "label", None) or button.get("action")

            pygame.draw.rect(
                self.screen,
                self.COLORS["button"],
                rect,
            )
            label = self.small_font.render(
                str(label_text).upper(),
                True,
                self.COLORS["text_primary"],
            )
            self.screen.blit(label, (rect.x + 10, rect.y + 10))
        return self.screen

    def draw_status(self, message, x, y):
        if not message:
            return self.screen

        label = self.small_font.render(
            str(message),
            True,
            self.COLORS["text_primary"],
        )
        background = pygame.Rect(
            x - 8,
            y - 6,
            label.get_width() + 16,
            label.get_height() + 12,
        )
        pygame.draw.rect(
            self.screen,
            self.COLORS["status_bg"],
            background,
        )
        self.screen.blit(label, (x, y))
        return self.screen
