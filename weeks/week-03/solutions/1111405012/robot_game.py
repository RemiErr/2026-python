import sys

import pygame

from robot_core import RobotWorld

# 世界格子大小（與 RobotWorld 對應）
GRID_W = 10
GRID_H = 10

# 視窗大小
WINDOW_W = 900
WINDOW_H = 520

# 每一格像素大小與邊界留白
CELL = 40
MARGIN = 28
PANEL_W = 350
BOTTOM_H = 150

# 顏色設定（RGB）
BG = (20, 24, 28)
GRID = (74, 84, 94)
ROBOT = (110, 240, 170)
SCENT = (220, 150, 90)
TEXT = (220, 230, 240)
PANEL_BG = (33, 39, 46)
PANEL_BORDER = (55, 62, 70)


def grid_to_screen(x: int, y: int) -> tuple[int, int]:
    # 將「格子座標」轉成「螢幕像素座標」
    sx = MARGIN + x * CELL + CELL // 2
    # y 軸要反轉：格子向上增加，但螢幕向下增加
    sy = MARGIN + (GRID_H - y) * CELL - CELL // 2
    return sx, sy


def cell_center(x: int, y: int) -> tuple[int, int]:
    draw_x = max(0, min(x, GRID_W - 1))
    draw_y = max(0, min(y, GRID_H - 1))
    sx = MARGIN + draw_x * CELL + CELL // 2
    sy = MARGIN + (GRID_H - 1 - draw_y) * CELL + CELL // 2
    return sx, sy


def draw_grid(screen: pygame.Surface) -> None:
    # 畫出直線與水平線形成網格
    for x in range(GRID_W + 1):
        sx = MARGIN + x * CELL
        pygame.draw.line(
            screen, GRID, (sx, MARGIN), (sx, MARGIN + GRID_H * CELL), 2
        )
    for y in range(GRID_H + 1):
        sy = MARGIN + y * CELL
        pygame.draw.line(
            screen, GRID, (MARGIN, sy), (MARGIN + GRID_W * CELL, sy), 2
        )


def draw_scents(screen: pygame.Surface, scents: set[tuple[int, int, str]]) -> None:
    # scents 只需要顯示座標，不需要方向
    for x, y, _dir in scents:
        center = cell_center(x, y)
        pygame.draw.circle(screen, SCENT, center, 8)


def draw_robot(screen: pygame.Surface, x: int, y: int, direction: str) -> None:
    # 用三角形表示機器人方向
    size = max(8, CELL // 3)
    inset = 4
    draw_x = max(0, min(x, GRID_W - 1))
    draw_y = max(0, min(y, GRID_H - 1))
    cell_left = MARGIN + draw_x * CELL + inset
    cell_right = MARGIN + (draw_x + 1) * CELL - inset
    cell_top = MARGIN + (GRID_H - 1 - draw_y) * CELL + inset
    cell_bottom = MARGIN + (GRID_H - draw_y) * CELL - inset
    sx = (cell_left + cell_right) // 2
    sy = (cell_top + cell_bottom) // 2
    size = min(size, (cell_right - cell_left) //
               2, (cell_bottom - cell_top) // 2)
    if direction == "N":
        tip = (sx, max(cell_top, sy - size))
        pts = [
            tip,
            (max(cell_left, sx - size), min(cell_bottom, sy + size)),
            (min(cell_right, sx + size), min(cell_bottom, sy + size)),
        ]
    elif direction == "S":
        tip = (sx, min(cell_bottom, sy + size))
        pts = [
            tip,
            (max(cell_left, sx - size), max(cell_top, sy - size)),
            (min(cell_right, sx + size), max(cell_top, sy - size)),
        ]
    elif direction == "E":
        tip = (min(cell_right, sx + size), sy)
        pts = [
            tip,
            (max(cell_left, sx - size), max(cell_top, sy - size)),
            (max(cell_left, sx - size), min(cell_bottom, sy + size)),
        ]
    else:
        tip = (max(cell_left, sx - size), sy)
        pts = [
            tip,
            (min(cell_right, sx + size), max(cell_top, sy - size)),
            (min(cell_right, sx + size), min(cell_bottom, sy + size)),
        ]
    pygame.draw.polygon(screen, ROBOT, pts)
    pygame.draw.circle(screen, TEXT, tip, max(3, size // 6))


def build_snapshot(world: RobotWorld, width: int, height: int) -> list[str]:
    grid = [["." for _ in range(width)] for _ in range(height)]
    for x, y, _dir in world.scents:
        if 0 <= x < width and 0 <= y < height:
            grid[height - 1 - y][x] = "S"
    rx, ry, _d, lost = world.state_tuple()
    if not lost and 0 <= rx < width and 0 <= ry < height:
        grid[height - 1 - ry][rx] = "R"
    return ["".join(row) for row in grid]


def draw_right_panel(
    screen: pygame.Surface,
    world: RobotWorld,
    font: pygame.font.Font,
    small_font: pygame.font.Font,
    last_event: str,
    command_log: str,
    robot_id: int,
) -> None:
    x, y, direction, lost = world.state_tuple()
    status = "LOST" if lost else "存活"

    def fit_text(text: str, max_width: int) -> str:
        if font.size(text)[0] <= max_width:
            return text
        clipped = text
        while clipped and font.size(clipped + "…")[0] > max_width:
            clipped = clipped[:-1]
        return clipped + "…" if clipped else ""

    max_text_width = PANEL_W - 24
    lines = [
        f"機器人 #{robot_id}: ({x},{y}) {direction} {status}",
        f"最新事件：{last_event}",
        f"Scent 數量：{len(world.scents)}",
        "回放影格數：0",
        f"指令紀錄：{command_log}",
        f"容器 world.scents (set) 觀察：",
        f"{sorted(world.scents)}",
    ]
    lines = [fit_text(line, max_text_width) for line in lines]

    panel_x = MARGIN * 2 + GRID_W * CELL
    panel_y = MARGIN
    panel_w = PANEL_W
    # 依內容自動計算面板高度，但不超過視窗可用高度
    line_h = 22
    title_gap = 6
    snap_h = 18
    padding = 12
    snapshot_rows = GRID_H
    needed_h = (
        padding * 2
        + line_h * len(lines)
        + title_gap
        + line_h
        + snap_h * snapshot_rows
    )
    max_h = WINDOW_H - MARGIN * 2
    panel_h = min(needed_h, max_h)
    pygame.draw.rect(
        screen,
        PANEL_BG,
        pygame.Rect(panel_x, panel_y, panel_w, panel_h),
        border_radius=12,
    )
    pygame.draw.rect(
        screen,
        PANEL_BORDER,
        pygame.Rect(panel_x, panel_y, panel_w, panel_h),
        width=2,
        border_radius=12,
    )

    text_y = panel_y + 12
    max_y = panel_y + panel_h - 12
    for text in lines:
        if text_y + 20 > max_y:
            break
        img = font.render(text, True, TEXT)
        screen.blit(img, (panel_x + 12, text_y))
        text_y += 22

    if text_y + 20 <= max_y:
        text_y += 6
        snapshot_title = f"{GRID_W}x{GRID_H} 矩陣快照"
        img = font.render(fit_text(snapshot_title, max_text_width), True, TEXT)
        screen.blit(img, (panel_x + 12, text_y))
        text_y += 22

    snapshot = build_snapshot(world, GRID_W, GRID_H)
    for row in snapshot:
        if text_y + 16 > max_y:
            break
        img = small_font.render(row, True, TEXT)
        screen.blit(img, (panel_x + 12, text_y))
        text_y += 18


def draw_bottom_panel(
    screen: pygame.Surface,
    world: RobotWorld,
    font: pygame.font.Font,
    small_font: pygame.font.Font,
) -> None:
    lines = [
        "操作：L/R/F 執行指令 | N 新機器人 | C 清除 scent | G 匯出 GIF | ESC 離開",
    ]
    text_y = MARGIN * 2 + GRID_H * CELL + 24
    for text in lines:
        img = font.render(text, True, TEXT)
        screen.blit(img, (MARGIN, text_y))
        text_y += 22


def main() -> None:
    # 初始化 pygame 與視窗
    pygame.init()
    width = WINDOW_W
    height = WINDOW_H
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Robot Lost (MVP)")
    # 嘗試使用繁體中文可顯示字型，失敗則退回英文字型
    font = pygame.font.SysFont("Microsoft JhengHei", 17)
    if not font:
        font = pygame.font.SysFont("consolas", 17)
    small_font = pygame.font.SysFont("Microsoft JhengHei", 15)
    if not small_font:
        small_font = pygame.font.SysFont("consolas", 15)

    # 建立世界與機器人
    # 畫面為 10x10，但邏輯座標為 0..9
    world = RobotWorld(GRID_W - 1, GRID_H - 1)

    clock = pygame.time.Clock()
    running = True
    last_event = "就緒"
    command_log = ""
    command_mxln = 15
    robot_id = 1
    while running:
        # 1. 事件處理（鍵盤/關閉視窗）
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key in (pygame.K_l, pygame.K_LEFT):
                    if not world.robot.lost:
                        last_event = world.step("L")
                        if len(command_log) >= command_mxln:
                            command_log = command_log[-command_mxln:]
                        command_log += "L"
                elif event.key in (pygame.K_r, pygame.K_RIGHT):
                    if not world.robot.lost:
                        last_event = world.step("R")
                        if len(command_log) >= command_mxln:
                            command_log = command_log[-command_mxln:]
                        command_log += "R"
                elif event.key in (pygame.K_f, pygame.K_UP):
                    if not world.robot.lost:
                        last_event = world.step("F")
                        if len(command_log) >= command_mxln:
                            command_log = command_log[-command_mxln:]
                        command_log += "F"
                elif event.key == pygame.K_n:
                    world.reset_robot(0, 0, "N")
                    last_event = "NEW_ROBOT"
                    command_log = ""
                    robot_id += 1
                elif event.key == pygame.K_c:
                    world.clear_scents()
                    last_event = "CLEAR_SCENTS"

        # 2. 畫面更新
        screen.fill(BG)
        draw_grid(screen)
        draw_scents(screen, world.scents)
        draw_robot(screen, world.robot.x, world.robot.y, world.robot.direction)
        draw_right_panel(screen, world, font, small_font,
                         last_event, command_log, robot_id)
        draw_bottom_panel(screen, world, font, small_font)
        pygame.display.flip()
        # 3. 控制 FPS
        clock.tick(30)

    # 離開時釋放資源
    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()
