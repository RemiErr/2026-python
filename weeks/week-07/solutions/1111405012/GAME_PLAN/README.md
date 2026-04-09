# GAME_PLAN Agent Spec

## 文件目的

本目錄是赤壁戰役作業的 Agent 開發規格，不是一般說明文件。

使用方式固定如下：

1. 先讀本文件，確認全域約束、可選路線、交付物與任務順序。
2. 再進入 `PLAN_TASKS/`，依任務文件逐項執行。
3. 任一 Agent 若只接手單一 TASK，也必須遵守本文件的全域規則。

---

## 專案簡述

本專案要在 `weeks/week-07/solutions/1111405012/` 完成一個符合 Week 02 與 Week 07 教學目標的赤壁戰役遊戲作業。

核心目標固定如下：

- 使用 Python 完成第一版可提交成果。
- 整合 Week 02 的 `sorted()`、`Counter`、`defaultdict`、`namedtuple`。
- 整合 Week 07 的檔案 I/O 與 EOF 處理。
- 依 TDD 流程完成核心邏輯、測試、日誌與報表。

進階目標可選，但不覆蓋主線：

- 加入 GUI 展示層。
- 將純計算核心抽成 C++ 或 Rust native 模組。

---

## 全域約束

以下規則對所有 TASK 都成立：

- 主線語言固定為 Python。
- 第一個可提交版本必須能在沒有 GUI、沒有 native 模組的情況下獨立執行。
- GUI 只能是展示層，不得直接承擔戰鬥邏輯。
- native 模組只能替換純計算區塊，不得接管 I/O、驗證、測試或報表。
- 所有進階方案都必須保留純 Python fallback。
- 所有資料檔預設放在 `weeks/week-07/`。
- 所有文件與程式預設採 UTF-8。

---

## 固定交付物

主線交付物：

- `weeks/week-07/solutions/1111405012/generals.txt`
- `weeks/week-07/solutions/1111405012/battles.txt`
- `weeks/week-07/solutions/1111405012/chibi_battle.py`
- `weeks/week-07/solutions/1111405012/chibi_battle_easy.py`
- `weeks/week-07/solutions/1111405012/test_chibi.py`
- `weeks/week-07/solutions/1111405012/TEST_LOG.md`
- `weeks/week-07/solutions/1111405012/AI_USAGE.md`

可選交付物：

- `weeks/week-07/solutions/1111405012/battle_gui.py`
- `weeks/week-07/solutions/1111405012/assets/`
- `weeks/week-07/solutions/1111405012/native/`

規劃與任務文件：

- `weeks/week-07/solutions/1111405012/GAME_PLAN/README.md`
- `weeks/week-07/solutions/1111405012/GAME_PLAN/PLAN_TASKS/`

---

## 資料與介面契約

固定資料結構：

- `General = namedtuple("General", ["faction", "name", "hp", "atk", "def_", "spd", "is_leader"])`
- `BattleConfig = namedtuple("BattleConfig", ["allies", "enemy", "battlefield", "waves"])`
- `BattleStats = {"damage": Counter(), "losses": defaultdict(int), "wave_logs": []}`
- `BattleResult = {"winner": "", "damage_ranking": [], "faction_stats": {}, "defeated_generals": [], "report_text": ""}`

固定核心 API：

- `load_generals(path)`
- `load_battles(path)`
- `get_battle_order()`
- `calculate_damage(attacker, defender)`
- `simulate_wave(wave_index)`
- `simulate_battle()`
- `get_damage_ranking(top_n=5)`
- `get_faction_stats()`
- `get_defeated_generals()`
- `render_ascii_report()`

GUI 可選 API：

- `build_view_model()`
- `step_battle()`
- `launch_gui()`

---

## 方案選擇

所有 Agent 都應先以 A 路線為基準，再視需求擴充。

| 路線 | 核心                | 介面        | 目標           |
| ---- | ------------------- | ----------- | -------------- |
| A    | Python              | CLI + ASCII | 穩定交作業     |
| B    | Python              | `tkinter`   | 最低成本 GUI   |
| C    | Python              | `pygame`    | 偏遊戲展示     |
| D    | Python + C++ DLL    | CLI 或 GUI  | 跨語言展示     |
| E    | Python + `pybind11` | `PySide6`   | 桌面應用工程版 |
| F    | Rust + `PyO3`       | `PySide6`   | 研究或作品集版 |

推薦順序：

1. A
2. C 或 B
3. D
4. E 或 F

---

## 任務執行順序

共同主線任務：

1. T01 專案骨架與資料契約
2. T02 資料模型、I/O 與驗證
3. T03 戰鬥核心與統計
4. T04 CLI 流程與 ASCII 報表
5. T05 測試、日誌與提交文件

可選分支任務：

6. T06 GUI 展示層方案
7. T07 Native 擴充方案

執行原則：

- T01 到 T05 是主線，不可跳過。
- T06 與 T07 只能在主線穩定後開始。
- 不要同時把 GUI 與 native 當作起始任務。

---

## 任務索引

| 任務 ID | 任務名稱              | 簡述                                   | 類型 | 依賴        |
| ------- | --------------------- | -------------------------------------- | ---- | ----------- |
| T01     | 專案骨架與資料契約    | 固定目錄、輸入檔格式與路徑規則         | 主線 | 無          |
| T02     | 資料模型、I/O 與驗證  | 建立資料結構、讀檔與輸入檢查           | 主線 | T01         |
| T03     | 戰鬥核心與統計        | 實作傷害、波次、排行與統計 API         | 主線 | T02         |
| T04     | CLI 流程與 ASCII 報表 | 建立可執行流程與文字版報表             | 主線 | T03         |
| T05     | 測試、日誌與提交文件  | 建立測試、開發日誌與 AI 使用說明       | 主線 | T02,T03,T04 |
| T06     | GUI 展示層方案        | 在不污染核心的前提下加入視窗或遊戲介面 | 分支 | T03,T04     |
| T07     | Native 擴充方案       | 將純計算部分抽成 C++ 或 Rust 模組      | 分支 | T03         |

詳細內容見 `PLAN_TASKS/README.md` 與各 TASK 文件。

---

## 全域完成定義

可視為完成的最低條件如下：

- 主線交付物都存在。
- 純 Python 版本可讀入資料並完成三波模擬。
- 至少有 12 個主測試。
- `TEST_LOG.md` 有 RED、GREEN、REFACTOR 記錄。
- 若選 GUI 或 native，主線版本仍能獨立運作。

---

## Agent 交接規則

若一個 Agent 只處理部分任務，交接內容至少要說清楚：

- 已完成哪些檔案或模組
- 仍未完成哪些項目
- 是否改動核心 API 或資料契約
- 是否新增了環境依賴
- 下一個 Agent 應從哪一個 TASK 接手
