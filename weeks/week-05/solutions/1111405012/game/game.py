from __future__ import annotations

try:
    from .ai import AIStrategy
    from .classifier import HandClassifier
    from .finder import HandFinder
    from .models import Card, Deck, Player
except ImportError:
    from ai import AIStrategy
    from classifier import HandClassifier
    from finder import HandFinder
    from models import Card, Deck, Player


class BigTwoGame:
    def __init__(self) -> None:
        self.deck = Deck()
        self.players: list[Player] = []
        self.current_player = 0
        self.last_play: list[Card] | tuple[list[Card], str] | None = None
        self.pass_count = 0
        self.winner: Player | None = None
        self.round_number = 1
        self.opening_required = True
        self.last_action_message = ""

    @staticmethod
    def _card_message(card: Card) -> str:
        suit_names = {
            0: "梅花",
            1: "方塊",
            2: "紅心",
            3: "黑桃",
        }
        rank_names = {
            3: "3",
            4: "4",
            5: "5",
            6: "6",
            7: "7",
            8: "8",
            9: "9",
            10: "10",
            11: "J",
            12: "Q",
            13: "K",
            14: "A",
            15: "2",
        }
        return f"{suit_names[card.suit]}{rank_names[card.rank]}"

    def setup(self) -> None:
        self.deck = Deck()
        self.deck.shuffle()

        self.players = [
            Player("Player1", False),
            Player("AI_1", True),
            Player("AI_2", True),
            Player("AI_3", True),
        ]

        for player in self.players:
            player.hand.clear()
            player.take_cards(self.deck.deal(13))
            player.hand.sort_desc()

        for index, player in enumerate(self.players):
            if player.hand.find_3_clubs() is not None:
                self.current_player = index
                break

        self.last_play = None
        self.pass_count = 0
        self.winner = None
        self.round_number = 1
        self.opening_required = True
        opener = self.players[self.current_player].name if self.players else "Player1"
        self.last_action_message = f"{opener} 先手，開局必須包含梅花 3。"

    def _last_play_cards(self) -> list[Card] | None:
        if self.last_play is None:
            return None
        if isinstance(self.last_play, tuple):
            return self.last_play[0]
        return self.last_play

    def _is_valid_play(self, cards: list[Card]) -> bool:
        last_play_cards = self._last_play_cards()
        if last_play_cards is None:
            if HandClassifier.classify(cards) is None:
                return False
            if self.opening_required:
                return any(card.rank == 3 and card.suit == 0 for card in cards)
            return True
        return HandClassifier.can_play(last_play_cards, cards)

    def validate_play(self, player: Player, cards: list[Card]) -> tuple[bool, str]:
        if not cards:
            return False, "請先選擇要出的牌。"

        if not self.players or self.get_current_player() is not player:
            return False, "現在不是你的回合。"

        if any(card not in player.hand for card in cards):
            return False, "選到的牌不在手牌中。"

        current = HandClassifier.classify(cards)
        if current is None:
            return False, "這不是合法牌型。"

        last_play_cards = self._last_play_cards()
        if last_play_cards is None:
            if self.opening_required and not any(
                card.rank == 3 and card.suit == 0 for card in cards
            ):
                return False, "開局第一手必須包含梅花 3。"
            return True, ""

        previous = HandClassifier.classify(last_play_cards)
        if previous is None:
            return False, "上一手牌的狀態異常。"

        if len(cards) != len(last_play_cards):
            return False, "出牌張數必須和上一手相同。"

        if len(cards) in (1, 2, 3) and current[0] != previous[0]:
            return False, "牌型必須和上一手相同。"

        if HandClassifier.compare(cards, last_play_cards) <= 0:
            return False, "這手牌無法壓過上一手。"

        return True, ""

    def play(self, player: Player, cards: list[Card]) -> bool:
        is_valid, message = self.validate_play(player, cards)
        if not is_valid:
            self.last_action_message = message
            return False

        played_cards = player.play_cards(cards)
        self.last_play = (played_cards, player.name)
        self.pass_count = 0
        self.opening_required = False
        self.check_winner()
        if self.is_game_over():
            self.last_action_message = f"{player.name} 獲勝。"
            return True

        cards_text = " ".join(self._card_message(card) for card in played_cards)
        self.last_action_message = f"{player.name} 出牌：{cards_text}"
        if not self.is_game_over():
            self.next_turn()
        return True

    def pass_(self, player: Player) -> bool:
        if not self.players or self.get_current_player() is not player:
            self.last_action_message = "現在不是你的回合。"
            return False

        if self._last_play_cards() is None:
            self.last_action_message = "目前不能 PASS，請先有人出牌。"
            return False

        self.pass_count += 1
        self.last_action_message = f"{player.name} PASS。"
        self.next_turn()
        self.check_round_reset()
        return True

    def next_turn(self) -> None:
        if not self.players:
            return
        self.current_player = (self.current_player + 1) % len(self.players)

    def check_round_reset(self) -> None:
        if self.pass_count >= max(1, len(self.players) - 1):
            self.last_play = None
            self.pass_count = 0
            self.round_number += 1
            self.last_action_message = "三家都 PASS，重新開始出牌。"

    def check_winner(self) -> Player | None:
        for player in self.players:
            if len(player.hand) == 0:
                self.winner = player
                return player
        return None

    def is_game_over(self) -> bool:
        return self.winner is not None

    def get_current_player(self) -> Player:
        return self.players[self.current_player]

    def ai_turn(self) -> bool:
        player = self.get_current_player()
        if not player.is_ai:
            return False

        valid_plays = HandFinder.get_all_valid_plays(
            player.hand,
            self._last_play_cards(),
            require_three_clubs=self.opening_required,
        )
        selected = AIStrategy.select_best(
            valid_plays,
            player.hand,
            is_first=self.opening_required,
        )
        if selected is None:
            return self.pass_(player)
        return self.play(player, selected)
