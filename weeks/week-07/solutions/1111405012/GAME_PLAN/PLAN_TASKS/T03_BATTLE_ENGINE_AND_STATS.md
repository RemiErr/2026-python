# T03 戰鬥核心與統計

## 簡述

完成可測試的戰鬥模擬核心，輸出傷害排行、勢力統計與戰敗名單。

## 任務目標

實作核心戰鬥 API，讓資料載入後能完成完整模擬，並產出穩定可驗證的統計結果。

## 前置依賴

- T02

## 輸入

- `General`
- `BattleConfig`
- `BattleStats`

## 產出

- `get_battle_order()`
- `calculate_damage(attacker, defender)`
- `simulate_wave(wave_index)`
- `simulate_battle()`
- `get_damage_ranking(top_n=5)`
- `get_faction_stats()`
- `get_defeated_generals()`

## 必做範圍

- 依速度排序出手順序
- 傷害公式固定為 `max(1, atk - def_)`
- 依 `waves` 執行多波模擬
- 同步更新 `damage` 與 `losses`
- 生成 `wave_logs`
- 產出排行、勢力統計、戰敗名單

## 非目標

- 不加入技能、暴擊、連擊等進階規則
- 不處理 GUI 動畫
- 不處理 native 邊界

## 執行步驟

1. 實作速度排序
2. 實作單次傷害計算
3. 實作單波戰鬥
4. 實作完整戰役
5. 實作統計查詢 API
6. 讓結果可被 CLI、GUI、測試共用

## 驗收標準

- 三波模擬能跑完
- 傷害統計不為空
- 排行為遞減排序
- 可得到勢力總傷害與戰敗名單

## 交接重點

- 不要把顯示邏輯混進本任務
- 不要把 GUI 狀態管理混進本任務
- 若新增欄位，必須同步更新上游資料契約
