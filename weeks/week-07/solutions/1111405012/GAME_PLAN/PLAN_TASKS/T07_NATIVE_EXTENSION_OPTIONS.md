# T07 Native 擴充方案

## 簡述

將純計算戰鬥核心抽成 C++ 或 Rust 模組，作為跨語言整合與效能展示的進階任務。

## 任務目標

建立 native 邊界、adapter 與 fallback 策略，確保進階方案不破壞主線 Python 版本。

## 前置依賴

- T03

## 輸入

- 穩定的核心戰鬥 API
- 可序列化的輸入輸出格式
- 主線純 Python 行為作為比對基準

## 產出

- `native/` 目錄規劃或實作骨架
- JSON 或 FFI 契約
- Python adapter 設計

## 必做範圍

- 定義 native 與 Python 的責任邊界
- 定義輸入輸出契約
- 定義 fallback 規則
- 定義結果一致性的驗收方式

## 非目標

- 不讓 native 模組接手 I/O
- 不讓 native 模組接手測試
- 不讓 native 模組變成主線唯一實作

## 可選技術

- C++ DLL + `ctypes` / `cffi`
- C++ + `pybind11`
- Rust + `PyO3` / `maturin`

## 執行步驟

1. 固定 native 只負責純計算
2. 選定 JSON 或 FFI 邊界
3. 規劃 `battle_core.dll` 或對應模組
4. 實作 Python adapter
5. 建立 fallback 到純 Python 的邏輯
6. 驗證 native 與 Python 結果一致

## 驗收標準

- native 失敗時主線仍可運作
- native 結果與 Python 結果一致
- 所有額外依賴都有明確說明

## 交接重點

- 說明選用的是 C++ 還是 Rust
- 說明是否需要補裝工具鏈
- 說明 adapter 與核心 API 的對接方式
