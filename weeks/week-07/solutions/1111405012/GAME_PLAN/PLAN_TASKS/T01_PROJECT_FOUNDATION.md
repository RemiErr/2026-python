# T01 專案骨架與資料契約

## 簡述

固定專案目錄、輸入檔格式與路徑規則，讓所有後續任務建立在同一份契約上。

## 任務目標

建立可實作的最小專案骨架，明確定義資料檔與提交目錄，避免後續實作依賴模糊假設。

## 前置依賴

- 無

## 輸入

- `weeks/week-07/HOMEWORK.md`
- `weeks/week-07/README.md`
- `GAME_PLAN/README.md`

## 產出

- `weeks/week-07/generals.txt`
- `weeks/week-07/battles.txt`
- `weeks/week-07/solutions/1111405012/` 的固定目錄結構

## 必做範圍

- 定義 `generals.txt` 欄位順序
- 定義 `battles.txt` 欄位順序
- 定義 UTF-8 與 EOF 規則
- 固定 week-07 與 solution 目錄之間的路徑關係

## 非目標

- 不實作戰鬥邏輯
- 不做 GUI
- 不做 native 模組

## 執行步驟

1. 確認 `generals.txt` 的格式為 `faction name hp atk def spd is_leader`
2. 確認 `battles.txt` 的格式為 `allies vs enemy battlefield waves`
3. 固定輸入檔編碼為 UTF-8
4. 固定 EOF 規則為單獨一行 `EOF`
5. 確認後續程式應從 `weeks/week-07/` 找資料檔

## 驗收標準

- 後續任務不需要再猜欄位順序
- 後續任務不需要再猜資料檔路徑
- 資料契約可直接被 T02 使用

## 交接重點

- 必須清楚說明資料檔放置位置
- 必須清楚說明 EOF 與空行處理規則
- 不要在本任務內引入任何 GUI 或 native 依賴
