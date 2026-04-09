# T04 CLI 流程與 ASCII 報表

## 簡述

將戰鬥核心包裝成可執行的文字版流程，並提供不改動狀態的 ASCII 報表。

## 任務目標

建立 CLI 主流程與 `render_ascii_report()`，讓專案在沒有 GUI 的情況下也能完整展示戰役結果。

## 前置依賴

- T03

## 輸入

- T03 的戰鬥結果
- `BattleStats`
- `BattleResult`

## 產出

- 文字版執行流程
- `render_ascii_report()`
- `chibi_battle_easy.py` 的簡化輸出流程

## 必做範圍

- 載入資料
- 啟動模擬
- 顯示波次摘要
- 顯示排行與勢力統計
- 產出 ASCII 報表

## 非目標

- 不在這一層處理 GUI 事件
- 不在這一層重算戰鬥邏輯
- 不加入 native 專屬流程

## 執行步驟

1. 規劃主程式輸出順序
2. 實作 `render_ascii_report()`
3. 保證報表只讀取資料，不寫回狀態
4. 以簡化方式包裝 `chibi_battle_easy.py`

## 驗收標準

- CLI 版本可單獨執行
- 報表輸出前後統計不變
- `chibi_battle_easy.py` 可輸出結果

## 交接重點

- 說明報表函式不能修改 `BattleStats`
- 說明簡化版與主版共享哪些邏輯
- GUI 任務應重用這一層結果，不重新實作統計
