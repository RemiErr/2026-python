from __future__ import annotations

import sys

# UVA 118 - 機器人（簡易版）
# 做法：逐台機器人模擬，記錄「掉落前位置 + 面向方向」的 scent
# 重點概念：
# 1. 世界範圍是 (0,0) 到 (max_x, max_y) 的矩形。
# 2. 指令包含 L（左轉）、R（右轉）、F（前進）。
# 3. 若前進會掉出邊界，機器人 LOST，並留下 scent。
# 4. 之後若有機器人在同一格、同一方向再嘗試掉出邊界，該 F 會被忽略。


def solve(input_str: str) -> str:
    # 去除空行，方便用兩行一組讀取機器人資料
    lines = [line.strip() for line in input_str.splitlines() if line.strip()]
    if not lines:
        return ""

    # 世界右上角座標
    max_x, max_y = map(int, lines[0].split())
    # scent 記錄「掉落前的位置 + 面向方向」
    scent = set()  # (x, y, dir)
    out = []

    i = 1
    while i < len(lines):
        # 讀取機器人初始位置與方向
        x, y, d = lines[i].split()
        x = int(x)
        y = int(y)
        i += 1

        # 讀取指令列
        cmds = lines[i] if i < len(lines) else ""
        i += 1

        lost = False
        for c in cmds:
            if c == "L":
                # 左轉 90 度
                d = {"N": "W", "W": "S", "S": "E", "E": "N"}[d]
            elif c == "R":
                # 右轉 90 度
                d = {"N": "E", "E": "S", "S": "W", "W": "N"}[d]
            elif c == "F":
                # 先計算前進後的位置
                nx, ny = x, y
                if d == "N":
                    ny += 1
                elif d == "S":
                    ny -= 1
                elif d == "E":
                    nx += 1
                else:
                    nx -= 1

                # 若會掉出邊界
                if nx < 0 or nx > max_x or ny < 0 or ny > max_y:
                    if (x, y, d) in scent:
                        # 有 scent 表示以前有人從這裡掉落，這次忽略
                        continue  # 有 scent 就忽略
                    # 否則留下 scent 並標記 LOST
                    scent.add((x, y, d))
                    lost = True
                    break
                else:
                    # 正常前進就更新位置
                    x, y = nx, ny

        if lost:
            out.append(f"{x} {y} {d} LOST")
        else:
            out.append(f"{x} {y} {d}")

    return "\n".join(out)


def main() -> None:
    data = sys.stdin.read()
    result = solve(data)
    if result:
        sys.stdout.write(result)


if __name__ == "__main__":
    main()
