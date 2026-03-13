# Robot Lost (Week 03)

## 功能清單
- 格子地圖顯示（10x10）
- 機器人位置/方向（三角形 + 頂點標示）
- scent 顯示（圓點）
- 鍵盤輸入 L/R/F 單步執行
- N 產生新機器人（保留 scent）
- C 清除 scent
- 右側資訊面板（狀態/事件/指令/矩陣快照）
- 底部操作提示

## 執行方式
1. Python 3.10+（建議）
2. 安裝 pygame

```bash
python -m pip install pygame
python robot_game.py
```

## 操作說明
- L / ←：左轉
- R / →：右轉
- F / ↑：前進
- N：新機器人（保留 scent）
- C：清除 scent
- ESC：離開

## 測試方式
```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

測試結果摘要：請更新 `TEST_LOG.md`。

## 資料結構選擇理由（至少 3 點）
1. `set[tuple[int, int, str]]` 紀錄 `scent`，查詢 O(1)，避免重複掉落。
2. `RobotState` 用 `dataclass` 讓狀態清楚、便於測試。
3. 方向與位移使用常數表，避免分支重複與錯誤。

## 一個 bug 與修正方式
- 問題：機器人貼近邊界時三角形會超出格子。
- 修正：以格子邊界計算三角形頂點，並加上內縮，確保不溢出。

## 遊玩截圖
請將截圖放入 `assets/gameplay.png`，並更新下方：

![gameplay](assets/gameplay.png)

## 重播方式說明
目前提供視覺回放區塊與指令紀錄（右側面板）。  
若要輸出 GIF，可在後續加入幀截圖與合成流程（例如：pygame 截圖 + imageio）。

