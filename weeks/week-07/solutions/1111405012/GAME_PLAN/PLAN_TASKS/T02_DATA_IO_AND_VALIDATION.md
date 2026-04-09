# T02 資料模型、I/O 與驗證

## 簡述

建立核心資料結構、讀檔函式與輸入驗證，讓遊戲引擎具備可靠的資料入口。

## 任務目標

完成 `General`、`BattleConfig`、`BattleStats`、`BattleResult` 的定義，並實作 `load_generals(path)`、`load_battles(path)` 與基本輸入檢查。

## 前置依賴

- T01

## 輸入

- T01 定義的資料契約
- `weeks/week-07/generals.txt`
- `weeks/week-07/battles.txt`

## 產出

- `chibi_battle.py` 中的資料模型
- `load_generals(path)`
- `load_battles(path)`
- 基本錯誤處理規則

## 必做範圍

- `General` 使用 `namedtuple`
- `BattleConfig` 使用 `namedtuple`
- `BattleStats` 使用 `Counter` 與 `defaultdict`
- `BattleResult` 使用字典型結構
- 讀取 UTF-8、空行、EOF
- 驗證欄位數量、整數欄位、布林欄位

## 非目標

- 不實作傷害計算
- 不實作報表
- 不引入 GUI
- 不引入 native 模組

## 執行步驟

1. 定義固定資料結構
2. 實作 `load_generals(path)` 並支援 EOF 停止
3. 實作 `load_battles(path)` 並支援波數解析
4. 加入空行略過與欄位驗證
5. 規範錯誤輸入時的回報方式

## 驗收標準

- 可正確讀到 9 位武將
- 可正確讀到 3 波戰役設定
- 欄位錯誤會有明確失敗訊息
- 這一層不依賴 GUI 或 native

## 交接重點

- 說明資料結構名稱與欄位不可任意改名
- 說明路徑處理方式
- 說明哪些錯誤是立即失敗，哪些是略過
