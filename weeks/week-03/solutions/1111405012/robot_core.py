from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

# 方向的順序很重要：左轉/右轉都靠這個循環
DIRECTIONS = ("N", "E", "S", "W")
# 方向對應的位移（dx, dy）
MOVE = {
    "N": (0, 1),
    "E": (1, 0),
    "S": (0, -1),
    "W": (-1, 0),
}


@dataclass
class RobotState:
    # 機器人在網格上的座標與方向
    x: int
    y: int
    direction: str
    # lost = True 代表已掉出邊界，後續指令都忽略
    lost: bool = False


class RobotWorld:
    def __init__(self, width: int, height: int) -> None:
        # 世界大小（座標從 0 到 width/height）
        if width < 0 or height < 0:
            raise ValueError("width/height must be >= 0")
        self.width = width
        self.height = height
        # scents 記錄「在某格面向某方向前進會掉出」的氣味
        self.scents: set[tuple[int, int, str]] = set()
        # 初始化機器人狀態
        self.robot = RobotState(0, 0, "N", False)

    def reset_robot(self, x: int = 0, y: int = 0, direction: str = "N") -> None:
        # 重新放置機器人
        if direction not in DIRECTIONS:
            raise ValueError("invalid direction")
        self.robot = RobotState(x, y, direction, False)

    def clear_scents(self) -> None:
        # 清除所有氣味（危險邊界的記錄）
        self.scents.clear()

    def turn_left(self) -> str:
        # 已掉出就忽略
        if self.robot.lost:
            return "IGNORED_LOST"
        idx = DIRECTIONS.index(self.robot.direction)
        # 左轉就是方向序列往前一格（用 %4 環狀）
        self.robot.direction = DIRECTIONS[(idx - 1) % 4]
        return "TURN_LEFT"

    def turn_right(self) -> str:
        # 已掉出就忽略
        if self.robot.lost:
            return "IGNORED_LOST"
        idx = DIRECTIONS.index(self.robot.direction)
        # 右轉就是方向序列往後一格
        self.robot.direction = DIRECTIONS[(idx + 1) % 4]
        return "TURN_RIGHT"

    def forward(self) -> str:
        # 已掉出就忽略
        if self.robot.lost:
            return "IGNORED_LOST"
        # 依方向計算下一格座標
        dx, dy = MOVE[self.robot.direction]
        next_x = self.robot.x + dx
        next_y = self.robot.y + dy

        # 超出邊界：可能掉出
        if next_x < 0 or next_x > self.width or next_y < 0 or next_y > self.height:
            scent_key = (self.robot.x, self.robot.y, self.robot.direction)
            # 如果這個位置/方向已經有氣味，代表以前有人掉過
            # 規則：有氣味就忽略這次前進
            if scent_key in self.scents:
                return "SCENT_BLOCKED"
            # 沒有氣味就記錄並讓機器人 LOST
            self.scents.add(scent_key)
            self.robot.lost = True
            return "LOST"

        # 正常移動
        self.robot.x = next_x
        self.robot.y = next_y
        return "MOVED"

    def step(self, command: str) -> str:
        # 單一步驟指令（只看第一個字元）
        if not command:
            return "INVALID"
        cmd = command[0].upper()
        if cmd == "L":
            return self.turn_left()
        if cmd == "R":
            return self.turn_right()
        if cmd == "F":
            return self.forward()
        return "INVALID"

    def execute(self, commands: Iterable[str]) -> RobotState:
        # 逐一執行指令字串/序列
        for cmd in commands:
            if self.robot.lost:
                # LOST 之後的指令都忽略
                break
            self.step(cmd)
        return self.robot

    def state_tuple(self) -> tuple[int, int, str, bool]:
        # 提供給外部顯示用的簡潔狀態
        return (self.robot.x, self.robot.y, self.robot.direction, self.robot.lost)
