from __future__ import annotations

import argparse
from collections import Counter, defaultdict, namedtuple
from pathlib import Path

General = namedtuple(
    "General",
    ["faction", "name", "hp", "atk", "def_", "spd", "is_leader"],
)
BattleConfig = namedtuple("BattleConfig", ["allies", "enemy", "battlefield", "waves"])

MODULE_DIR = Path(__file__).resolve().parent
WEEK_DIR = MODULE_DIR.parent.parent
DEFAULT_GENERALS_PATH = WEEK_DIR / "generals.txt"
DEFAULT_BATTLES_PATH = WEEK_DIR / "battles.txt"


def _make_battle_stats():
    return {
        "damage": Counter(),
        "losses": defaultdict(int),
        "wave_logs": [],
    }


def _make_battle_result():
    return {
        "winner": "",
        "damage_ranking": [],
        "faction_stats": {},
        "defeated_generals": [],
        "report_text": "",
    }


class GameExitRequested(Exception):
    pass


def _resolve_input_path(path):
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate

    search_paths = [
        Path.cwd() / candidate,
        WEEK_DIR / candidate,
        MODULE_DIR / candidate,
    ]

    if candidate.parent != Path("."):
        search_paths.extend(
            [
                WEEK_DIR / candidate.name,
                MODULE_DIR / candidate.name,
            ]
        )

    seen = set()
    for item in search_paths:
        normalized = str(item.resolve(strict=False))
        if normalized in seen:
            continue
        seen.add(normalized)
        if item.exists():
            return item

    return search_paths[0]


def _iter_data_lines(path):
    resolved_path = _resolve_input_path(path)
    with resolved_path.open("r", encoding="utf-8") as handle:
        for line_number, raw_line in enumerate(handle, start=1):
            line = raw_line.strip()
            if not line:
                continue
            if line == "EOF":
                break
            yield line_number, line


def _parse_int(value, field_name, line_number):
    try:
        return int(value)
    except ValueError as exc:
        raise ValueError(
            f"Invalid integer for {field_name} on line {line_number}: {value}"
        ) from exc


def _parse_bool(value, field_name, line_number):
    if value not in {"True", "False"}:
        raise ValueError(
            f"Invalid boolean for {field_name} on line {line_number}: {value}"
        )
    return value == "True"


def load_generals(path=DEFAULT_GENERALS_PATH):
    generals = {}

    for line_number, line in _iter_data_lines(path):
        parts = line.split()
        if len(parts) != 7:
            raise ValueError(
                f"Invalid general field count on line {line_number}: expected 7, got {len(parts)}"
            )

        faction, name, hp, atk, def_, spd, is_leader = parts
        if name in generals:
            raise ValueError(f"Duplicate general name on line {line_number}: {name}")

        generals[name] = General(
            faction=faction,
            name=name,
            hp=_parse_int(hp, "hp", line_number),
            atk=_parse_int(atk, "atk", line_number),
            def_=_parse_int(def_, "def_", line_number),
            spd=_parse_int(spd, "spd", line_number),
            is_leader=_parse_bool(is_leader, "is_leader", line_number),
        )

    return generals


def load_battles(path=DEFAULT_BATTLES_PATH):
    configs = []

    for line_number, line in _iter_data_lines(path):
        parts = line.split()
        if len(parts) != 5:
            raise ValueError(
                f"Invalid battle field count on line {line_number}: expected 5, got {len(parts)}"
            )

        allies, vs_token, enemy, battlefield, waves = parts
        if vs_token != "vs":
            raise ValueError(
                f"Invalid battle separator on line {line_number}: expected 'vs', got {vs_token}"
            )

        configs.append(
            BattleConfig(
                allies=allies,
                enemy=enemy,
                battlefield=battlefield,
                waves=_parse_int(waves, "waves", line_number),
            )
        )

    if not configs:
        raise ValueError("No battle configuration found in battles file")

    return configs[0]


class ChibiBattle:
    def __init__(self):
        self.generals = {}
        self.battle_config = None
        self.stats = _make_battle_stats()
        self.result = _make_battle_result()
        self.current_hp = {}

    def reset_battle_state(self):
        self.stats = _make_battle_stats()
        self.result = _make_battle_result()
        self.current_hp = {name: general.hp for name, general in self.generals.items()}

    def load_generals(self, path=DEFAULT_GENERALS_PATH):
        self.generals = load_generals(path)
        self.reset_battle_state()
        return self.generals

    def load_battles(self, path=DEFAULT_BATTLES_PATH):
        self.battle_config = load_battles(path)
        return self.battle_config

    def _ensure_generals(self):
        if not self.generals:
            self.load_generals(DEFAULT_GENERALS_PATH)

    def _ensure_battle_config(self):
        if self.battle_config is None:
            self.load_battles(DEFAULT_BATTLES_PATH)
        return self.battle_config

    def _resolve_general(self, general):
        if isinstance(general, General):
            return general
        if hasattr(general, "name"):
            return self.generals[general.name]
        return self.generals[str(general)]

    def _is_ally(self, general):
        return general.faction in self.battle_config.allies

    def _factions_for_side(self, side_name):
        if side_name == self.battle_config.enemy:
            return {self.battle_config.enemy}
        return set(self.battle_config.allies)

    def _living_generals_for_side(self, side_name):
        self._ensure_generals()
        self._ensure_battle_config()
        factions = self._factions_for_side(side_name)

        return [
            general
            for general in self.generals.values()
            if general.faction in factions and self.current_hp.get(general.name, general.hp) > 0
        ]

    def _all_generals_for_side(self, side_name):
        self._ensure_generals()
        self._ensure_battle_config()
        factions = self._factions_for_side(side_name)
        members = [
            general for general in self.generals.values() if general.faction in factions
        ]
        return sorted(members, key=lambda general: (general.faction, -general.spd, general.name))

    def _get_remaining_hp(self, side_name):
        return sum(
            self.current_hp.get(general.name, general.hp)
            for general in self._living_generals_for_side(side_name)
        )

    def _select_target(self, candidates):
        return sorted(
            candidates,
            key=lambda general: (
                self.current_hp[general.name],
                -general.spd,
                general.name,
            ),
        )[0]

    def _perform_attack(self, attacker, defender):
        damage = self.calculate_damage(attacker, defender)
        attacker_ref = self._resolve_general(attacker)
        defender_ref = self._resolve_general(defender)
        remaining_hp = self.current_hp[defender_ref.name]
        return {
            "attacker": attacker_ref.name,
            "defender": defender_ref.name,
            "damage": damage,
            "defender_hp": remaining_hp,
            "defeated": remaining_hp == 0,
        }

    def _build_wave_log(self, wave_index, turns):
        return {
            "wave": wave_index,
            "turns": turns,
            "allies_alive": len(self._living_generals_for_side(self.battle_config.allies)),
            "enemy_alive": len(self._living_generals_for_side(self.battle_config.enemy)),
            "allies_hp": self._get_remaining_hp(self.battle_config.allies),
            "enemy_hp": self._get_remaining_hp(self.battle_config.enemy),
        }

    def _format_turn_text(self, turn):
        status = "擊破" if turn["defeated"] else f"剩餘 {turn['defender_hp']} HP"
        return (
            f"{turn['attacker']} -> {turn['defender']} "
            f"造成 {turn['damage']} 傷害，{status}"
        )

    def render_status_panel(self):
        self._ensure_generals()
        self._ensure_battle_config()

        lines = []
        for side_name, title in (
            (self.battle_config.allies, f"盟軍 {self.battle_config.allies}"),
            (self.battle_config.enemy, f"敵軍 {self.battle_config.enemy}"),
        ):
            lines.append(f"[{title}]")
            for general in self._all_generals_for_side(side_name):
                current_hp = self.current_hp.get(general.name, general.hp)
                filled = int((current_hp / general.hp) * 10) if general.hp else 0
                bar = "#" * filled + "." * (10 - filled)
                leader_tag = " 軍師" if general.is_leader else ""
                defeated_tag = " 已退場" if current_hp == 0 else ""
                lines.append(
                    f"- {general.name:<6} {bar} {current_hp:>3}/{general.hp:<3} "
                    f"攻{general.atk:>2} 防{general.def_:>2} 速{general.spd:>2}"
                    f"{leader_tag}{defeated_tag}"
                )
        return "\n".join(lines)

    def _prompt_player_target(self, attacker, candidates, input_func=input, output_func=print):
        output_func("")
        output_func(f"輪到 {attacker.name} 出手。")
        for index, target in enumerate(candidates, start=1):
            current_hp = self.current_hp[target.name]
            output_func(
                f"{index}. {target.name} ({target.faction}) "
                f"HP {current_hp}/{target.hp} 防{target.def_}"
            )

        while True:
            choice = input_func("請輸入目標編號或名字，離開請輸入 q: ").strip()
            if choice.lower() in {"q", "quit", "exit"}:
                raise GameExitRequested("玩家中止遊戲")

            if choice.isdigit():
                selected_index = int(choice)
                if 1 <= selected_index <= len(candidates):
                    return candidates[selected_index - 1]
            else:
                for target in candidates:
                    if choice == target.name:
                        return target

            output_func("無效的目標，請重新輸入。")

    def _run_wave(self, wave_index, target_selector, output_func=None):
        self._ensure_generals()
        self._ensure_battle_config()
        if not self.current_hp:
            self.reset_battle_state()
        if wave_index < 1:
            raise ValueError("wave_index must be at least 1")

        turns = []
        for attacker in self.get_battle_order():
            if self.current_hp[attacker.name] <= 0:
                continue

            if self._is_ally(attacker):
                candidates = self._living_generals_for_side(self.battle_config.enemy)
            else:
                candidates = self._living_generals_for_side(self.battle_config.allies)

            if not candidates:
                break

            target = target_selector(attacker, candidates)
            turn = self._perform_attack(attacker, target)
            turns.append(turn)

            if output_func is not None:
                output_func(self._format_turn_text(turn))

            allies_alive = self._living_generals_for_side(self.battle_config.allies)
            enemies_alive = self._living_generals_for_side(self.battle_config.enemy)
            if not allies_alive or not enemies_alive:
                break

        wave_log = self._build_wave_log(wave_index, turns)
        self.stats["wave_logs"].append(wave_log)
        return wave_log

    def get_battle_order(self):
        self._ensure_generals()
        if not self.current_hp:
            self.reset_battle_state()

        living = [
            general
            for general in self.generals.values()
            if self.current_hp.get(general.name, general.hp) > 0
        ]
        return sorted(living, key=lambda general: (-general.spd, general.name))

    def calculate_damage(self, attacker, defender):
        self._ensure_generals()
        if not self.current_hp:
            self.reset_battle_state()

        attacker_ref = self._resolve_general(attacker)
        defender_ref = self._resolve_general(defender)

        damage = max(1, attacker_ref.atk - defender_ref.def_)
        self.stats["damage"][attacker_ref.name] += damage
        self.stats["losses"][defender_ref.name] += damage
        self.current_hp[defender_ref.name] = max(
            0,
            self.current_hp.get(defender_ref.name, defender_ref.hp) - damage,
        )
        return damage

    def simulate_wave(self, wave_index):
        return self._run_wave(
            wave_index,
            target_selector=lambda _attacker, candidates: self._select_target(candidates),
        )

    def play_wave(self, wave_index, input_func=input, output_func=print):
        self._ensure_generals()
        self._ensure_battle_config()

        output_func("")
        output_func("=" * 60)
        output_func(f"第 {wave_index} 波開始")
        output_func("=" * 60)
        output_func(self.render_status_panel())

        def target_selector(attacker, candidates):
            if self._is_ally(attacker):
                return self._prompt_player_target(
                    attacker,
                    candidates,
                    input_func=input_func,
                    output_func=output_func,
                )

            target = self._select_target(candidates)
            output_func(f"{attacker.name} 自動鎖定 {target.name}")
            return target

        wave_log = self._run_wave(
            wave_index,
            target_selector=target_selector,
            output_func=output_func,
        )
        output_func(
            f"第 {wave_index} 波結束: 盟軍剩餘 {wave_log['allies_hp']} HP, "
            f"敵軍剩餘 {wave_log['enemy_hp']} HP"
        )
        return wave_log

    def simulate_battle(self):
        self._ensure_generals()
        self._ensure_battle_config()
        self.reset_battle_state()

        for wave_index in range(1, self.battle_config.waves + 1):
            self.simulate_wave(wave_index)

        self.result = {
            "winner": self._determine_winner(),
            "damage_ranking": self.get_damage_ranking(),
            "faction_stats": self.get_faction_stats(),
            "defeated_generals": self.get_defeated_generals(),
            "report_text": self.render_ascii_report(),
        }
        return self.result

    def play_game(self, input_func=input, output_func=print):
        self._ensure_generals()
        self._ensure_battle_config()
        self.reset_battle_state()

        output_func("=" * 60)
        output_func("赤壁戰役互動模式")
        output_func(f"你將指揮 {self.battle_config.allies} 聯軍，在每個盟軍回合決定攻擊目標。")
        output_func("輸入數字或武將名字選擇目標，輸入 q 可離開。")
        output_func("=" * 60)

        for wave_index in range(1, self.battle_config.waves + 1):
            if not self._living_generals_for_side(self.battle_config.allies):
                break
            if not self._living_generals_for_side(self.battle_config.enemy):
                break
            self.play_wave(wave_index, input_func=input_func, output_func=output_func)

        self.result = {
            "winner": self._determine_winner(),
            "damage_ranking": self.get_damage_ranking(),
            "faction_stats": self.get_faction_stats(),
            "defeated_generals": self.get_defeated_generals(),
            "report_text": self.render_ascii_report(),
        }

        output_func("")
        output_func(self.result["report_text"])
        return self.result

    def _determine_winner(self):
        allies_hp = self._get_remaining_hp(self.battle_config.allies)
        enemy_hp = self._get_remaining_hp(self.battle_config.enemy)

        if allies_hp > enemy_hp:
            return self.battle_config.allies
        if enemy_hp > allies_hp:
            return self.battle_config.enemy
        return "平手"

    def get_damage_ranking(self, top_n=5):
        return self.stats["damage"].most_common(top_n)

    def get_faction_stats(self):
        totals = defaultdict(int)
        for general_name, damage in self.stats["damage"].items():
            totals[self.generals[general_name].faction] += damage

        for faction in {general.faction for general in self.generals.values()}:
            totals[faction] += 0

        return dict(sorted(totals.items()))

    def get_defeated_generals(self):
        return [
            name
            for name in self.generals
            if self.current_hp.get(name, self.generals[name].hp) <= 0
        ]

    def render_ascii_report(self):
        self._ensure_generals()
        self._ensure_battle_config()

        lines = [
            "=" * 60,
            f"赤壁戰役報表  戰場: {self.battle_config.battlefield}",
            "=" * 60,
            f"盟軍: {self.battle_config.allies}",
            f"敵軍: {self.battle_config.enemy}",
            f"總波數: {self.battle_config.waves}",
            f"勝方: {self._determine_winner()}",
            "",
            "Wave Summary",
        ]

        if self.stats["wave_logs"]:
            for wave_log in self.stats["wave_logs"]:
                lines.append(
                    f"- Wave {wave_log['wave']}: "
                    f"{len(wave_log['turns'])} turns, "
                    f"allies_alive={wave_log['allies_alive']}, "
                    f"enemy_alive={wave_log['enemy_alive']}"
                )
        else:
            lines.append("- 尚未執行戰鬥")

        lines.extend(["", "Damage Ranking"])
        ranking = self.get_damage_ranking()
        if ranking:
            max_damage = ranking[0][1]
            for index, (name, damage) in enumerate(ranking, start=1):
                bar_length = int((damage / max_damage) * 20) if max_damage else 0
                bar = "#" * bar_length + "." * (20 - bar_length)
                lines.append(f"{index}. {name:<6} {bar} {damage}")
        else:
            lines.append("- 無傷害資料")

        lines.extend(["", "Faction Damage"])
        faction_stats = self.get_faction_stats()
        max_faction_damage = max(faction_stats.values(), default=0)
        for faction, total in faction_stats.items():
            bar_length = int((total / max_faction_damage) * 20) if max_faction_damage else 0
            bar = "#" * bar_length + "." * (20 - bar_length)
            lines.append(f"- {faction}: {bar} {total}")

        lines.extend(["", "Defeated Generals"])
        defeated = self.get_defeated_generals()
        if defeated:
            for name in defeated:
                lines.append(f"- {name}")
        else:
            lines.append("- 無")

        return "\n".join(lines)


def build_default_game():
    game = ChibiBattle()
    game.load_generals(DEFAULT_GENERALS_PATH)
    game.load_battles(DEFAULT_BATTLES_PATH)
    return game


def run_cli(generals_path=DEFAULT_GENERALS_PATH, battles_path=DEFAULT_BATTLES_PATH):
    game = ChibiBattle()
    game.load_generals(generals_path)
    game.load_battles(battles_path)
    game.simulate_battle()
    return game.render_ascii_report()


def run_interactive_cli(
    generals_path=DEFAULT_GENERALS_PATH,
    battles_path=DEFAULT_BATTLES_PATH,
    input_func=input,
    output_func=print,
):
    game = ChibiBattle()
    game.load_generals(generals_path)
    game.load_battles(battles_path)
    return game.play_game(input_func=input_func, output_func=output_func)


def main(argv=None):
    parser = argparse.ArgumentParser(description="赤壁戰役 CLI 模擬器")
    parser.add_argument("--generals", default=str(DEFAULT_GENERALS_PATH))
    parser.add_argument("--battles", default=str(DEFAULT_BATTLES_PATH))
    parser.add_argument("--mode", choices=["auto", "play"], default="play")
    args = parser.parse_args(argv)

    try:
        if args.mode == "play":
            run_interactive_cli(args.generals, args.battles)
        else:
            print(run_cli(args.generals, args.battles))
    except GameExitRequested:
        print("遊戲已中止。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
