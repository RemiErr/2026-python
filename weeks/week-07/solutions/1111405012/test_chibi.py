from __future__ import annotations

import copy
import sys
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

import chibi_battle_easy  # noqa: E402

from chibi_battle import (  # noqa: E402
    BattleConfig,
    ChibiBattle,
    DEFAULT_BATTLES_PATH,
    DEFAULT_GENERALS_PATH,
    GameExitRequested,
    General,
    load_battles,
    load_generals,
    main,
    run_interactive_cli,
)


class ChibiBattleTestCase(unittest.TestCase):
    def setUp(self):
        self.game = ChibiBattle()
        self.game.load_generals(DEFAULT_GENERALS_PATH)
        self.game.load_battles(DEFAULT_BATTLES_PATH)


class TestDataLoading(ChibiBattleTestCase):
    def test_load_generals_reads_nine_generals(self):
        self.assertEqual(len(self.game.generals), 9)
        self.assertIn("劉備", self.game.generals)
        self.assertIn("曹操", self.game.generals)

    def test_load_generals_parses_namedtuple_fields(self):
        general = self.game.generals["關羽"]
        self.assertIsInstance(general, General)
        self.assertEqual(general.faction, "蜀")
        self.assertEqual(general.atk, 28)
        self.assertEqual(general.def_, 14)
        self.assertEqual(general.spd, 85)
        self.assertFalse(general.is_leader)

    def test_load_battles_parses_config(self):
        config = self.game.battle_config
        self.assertIsInstance(config, BattleConfig)
        self.assertEqual(config.allies, "蜀吳")
        self.assertEqual(config.enemy, "魏")
        self.assertEqual(config.battlefield, "赤壁")
        self.assertEqual(config.waves, 3)

    def test_load_generals_stops_at_eof(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            sample_path = Path(temp_dir) / "generals.txt"
            sample_path.write_text(
                "蜀 劉備 100 18 16 75 False\nEOF\n魏 曹操 120 28 16 80 False\n",
                encoding="utf-8",
            )

            generals = load_generals(sample_path)

        self.assertEqual(list(generals.keys()), ["劉備"])

    def test_invalid_general_field_count_raises_value_error(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            sample_path = Path(temp_dir) / "generals.txt"
            sample_path.write_text("蜀 劉備 100 18 16 75\nEOF\n", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "field count"):
                load_generals(sample_path)

    def test_invalid_general_boolean_raises_value_error(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            sample_path = Path(temp_dir) / "generals.txt"
            sample_path.write_text(
                "蜀 劉備 100 18 16 75 Maybe\nEOF\n",
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ValueError, "Invalid boolean"):
                load_generals(sample_path)

    def test_invalid_battle_separator_raises_value_error(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            sample_path = Path(temp_dir) / "battles.txt"
            sample_path.write_text("蜀吳 against 魏 赤壁 3\nEOF\n", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "separator"):
                load_battles(sample_path)


class TestBattleEngine(ChibiBattleTestCase):
    def test_get_battle_order_sorted_by_speed_descending(self):
        order = self.game.get_battle_order()
        speeds = [general.spd for general in order]
        self.assertEqual(speeds, sorted(speeds, reverse=True))
        self.assertEqual(order[0].spd, 85)
        self.assertEqual(order[-1].spd, 60)

    def test_calculate_damage_uses_minimum_one(self):
        damage = self.game.calculate_damage("諸葛亮", "曹操")
        self.assertEqual(damage, 1)

    def test_calculate_damage_updates_damage_and_losses(self):
        damage = self.game.calculate_damage("關羽", "夏侯惇")
        self.assertEqual(damage, 14)
        self.assertEqual(self.game.stats["damage"]["關羽"], 14)
        self.assertEqual(self.game.stats["losses"]["夏侯惇"], 14)
        self.assertEqual(self.game.current_hp["夏侯惇"], 91)

    def test_simulate_wave_records_wave_log(self):
        wave_log = self.game.simulate_wave(1)
        self.assertEqual(wave_log["wave"], 1)
        self.assertGreater(len(wave_log["turns"]), 0)
        self.assertEqual(len(self.game.stats["wave_logs"]), 1)

    def test_simulate_battle_runs_three_waves(self):
        result = self.game.simulate_battle()
        self.assertEqual(len(self.game.stats["wave_logs"]), 3)
        self.assertEqual(self.game.stats["wave_logs"][-1]["wave"], 3)
        self.assertEqual(result["winner"], "蜀吳")

    def test_damage_ranking_is_descending(self):
        self.game.simulate_battle()
        ranking = self.game.get_damage_ranking()
        damages = [damage for _, damage in ranking]
        self.assertEqual(damages, sorted(damages, reverse=True))

    def test_get_faction_stats_has_positive_damage(self):
        self.game.simulate_battle()
        faction_stats = self.game.get_faction_stats()
        self.assertGreater(faction_stats["蜀"], 0)
        self.assertGreater(faction_stats["吳"], 0)
        self.assertGreater(faction_stats["魏"], 0)

    def test_get_defeated_generals_after_three_waves(self):
        self.game.simulate_battle()
        defeated = self.game.get_defeated_generals()
        self.assertGreaterEqual(len(defeated), 1)
        self.assertIn("郭嘉", defeated)

    def test_render_ascii_report_does_not_mutate_state(self):
        self.game.simulate_battle()
        snapshot = {
            "damage": copy.deepcopy(self.game.stats["damage"]),
            "losses": copy.deepcopy(dict(self.game.stats["losses"])),
            "wave_logs": copy.deepcopy(self.game.stats["wave_logs"]),
            "current_hp": copy.deepcopy(self.game.current_hp),
            "result": copy.deepcopy(self.game.result),
        }

        report = self.game.render_ascii_report()

        self.assertIn("赤壁戰役報表", report)
        self.assertEqual(self.game.stats["damage"], snapshot["damage"])
        self.assertEqual(dict(self.game.stats["losses"]), snapshot["losses"])
        self.assertEqual(self.game.stats["wave_logs"], snapshot["wave_logs"])
        self.assertEqual(self.game.current_hp, snapshot["current_hp"])
        self.assertEqual(self.game.result, snapshot["result"])

    def test_play_wave_uses_player_selected_target(self):
        outputs = []
        self.game.play_wave(
            1,
            input_func=lambda _prompt: "2",
            output_func=outputs.append,
        )

        first_turn = self.game.stats["wave_logs"][0]["turns"][0]
        self.assertEqual(first_turn["attacker"], "周瑜")
        self.assertEqual(first_turn["defender"], "夏侯惇")
        self.assertIn("輪到 周瑜 出手。", outputs)

    def test_play_game_can_finish_with_stub_inputs(self):
        outputs = []
        scripted_inputs = iter(["1"] * 30)

        result = self.game.play_game(
            input_func=lambda _prompt: next(scripted_inputs),
            output_func=outputs.append,
        )

        self.assertIn(result["winner"], {"蜀吳", "魏", "平手"})
        self.assertTrue(any("赤壁戰役互動模式" in line for line in outputs))
        self.assertEqual(len(self.game.stats["wave_logs"]), 3)

    def test_run_interactive_cli_propagates_exit_request(self):
        with self.assertRaises(GameExitRequested):
            run_interactive_cli(
                DEFAULT_GENERALS_PATH,
                DEFAULT_BATTLES_PATH,
                input_func=lambda _prompt: "q",
                output_func=lambda _line: None,
            )

    def test_main_defaults_to_play_mode(self):
        with patch("chibi_battle.run_interactive_cli") as interactive_mock:
            exit_code = main([])

        interactive_mock.assert_called_once()
        self.assertEqual(exit_code, 0)

    def test_easy_main_defaults_to_play_mode(self):
        with patch("chibi_battle_easy.run_interactive_cli") as interactive_mock:
            exit_code = chibi_battle_easy.main([])

        interactive_mock.assert_called_once()
        self.assertEqual(exit_code, 0)


if __name__ == "__main__":
    unittest.main()
