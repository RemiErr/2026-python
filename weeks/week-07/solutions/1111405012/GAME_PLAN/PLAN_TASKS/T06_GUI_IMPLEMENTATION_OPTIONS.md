# T06 GUI 展示層方案

## 簡述

在不改動核心戰鬥規則的前提下，加入圖形化展示層，支援視窗操作與更直觀的戰役呈現。

## 任務目標

建立 GUI 封裝策略與實作方向，讓核心邏輯能被 `tkinter`、`pygame` 或 `PySide6` 消費。

## 前置依賴

- T03
- T04

## 輸入

- 核心 API
- CLI 可用的戰鬥結果
- `BattleResult` 或 `view_model`

## 產出

- `battle_gui.py`
- 可選的 `assets/`
- GUI 專用的 `build_view_model()`、`step_battle()`、`launch_gui()`

## 必做範圍

- 選定 GUI 技術
- 規劃畫面區塊
- 規劃按鈕與互動
- 保持 GUI 與核心分離

## 非目標

- 不在 GUI 層重寫傷害公式
- 不在 GUI 層重算統計
- 不把 GUI 當成主線必要條件

## 可選技術

- `tkinter`: 低成本桌面 GUI
- `pygame`: 偏遊戲感展示
- `PySide6`: 較完整的桌面應用元件

## 執行步驟

1. 選定 GUI 框架
2. 定義 `view_model` 與事件流
3. 建立資訊顯示區、波次區、結果區
4. 實作開始、單步、重置
5. 視需求加入資產與動畫

## 驗收標準

- 關閉 GUI 後主線仍可運作
- GUI 能展示完整戰役或單步流程
- GUI 不直接依賴未公開的內部狀態結構

## 交接重點

- 指明選的是哪個 GUI 框架
- 說明 `battle_gui.py` 依賴哪些核心 API
- 說明是否新增了外部資產或套件
