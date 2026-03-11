from __future__ import annotations

import sys
from typing import Dict, List, Set, Tuple

# UVA 118 - Mutant Flatworld Explorers
# 解題重點：依序處理機器人，並記錄「掉落前的位置 + 方向」的 scent，
# 之後若有機器人在同一格同方向再往外走，必須忽略該指令。


def _turn_left(direction: str) -> str:
    """向左轉 90 度。"""
    return {"N": "W", "W": "S", "S": "E", "E": "N"}[direction]


def _turn_right(direction: str) -> str:
    """向右轉 90 度。"""
    return {"N": "E", "E": "S", "S": "W", "W": "N"}[direction]


def _forward(x: int, y: int, direction: str) -> Tuple[int, int]:
    """依方向前進一格。"""
    if direction == "N":
        return x, y + 1
    if direction == "S":
        return x, y - 1
    if direction == "E":
        return x + 1, y
    return x - 1, y


def solve(input_str: str) -> str:
    """處理輸入字串並回傳輸出字串。"""
    # 移除空行，方便以「兩行一組」讀取機器人資料
    lines = [line.strip() for line in input_str.splitlines() if line.strip() != ""]
    if not lines:
        return ""

    # 讀取世界右上角座標
    max_x, max_y = map(int, lines[0].split())

    # scent 記錄「掉落前位置 + 面向方向」，避免重複掉落
    scent: Set[Tuple[int, int, str]] = set()
    outputs: List[str] = []

    idx = 1
    while idx < len(lines):
        # 機器人初始狀態
        x_str, y_str, direction = lines[idx].split()
        x = int(x_str)
        y = int(y_str)
        idx += 1

        # 指令列
        instructions = lines[idx].strip() if idx < len(lines) else ""
        idx += 1

        lost = False
        for cmd in instructions:
            if cmd == "L":
                direction = _turn_left(direction)
            elif cmd == "R":
                direction = _turn_right(direction)
            elif cmd == "F":
                nx, ny = _forward(x, y, direction)
                # 若會掉出邊界
                if nx < 0 or nx > max_x or ny < 0 or ny > max_y:
                    # 若有 scent，忽略此指令
                    if (x, y, direction) in scent:
                        continue
                    # 否則標記並宣告 LOST
                    scent.add((x, y, direction))
                    lost = True
                    break
                else:
                    # 正常前進
                    x, y = nx, ny

        if lost:
            outputs.append(f"{x} {y} {direction} LOST")
        else:
            outputs.append(f"{x} {y} {direction}")

    return "\n".join(outputs)


def main() -> None:
    """stdin/stdout 介面。"""
    data = sys.stdin.read()
    output = solve(data)
    if output:
        sys.stdout.write(output)


if __name__ == "__main__":
    main()
