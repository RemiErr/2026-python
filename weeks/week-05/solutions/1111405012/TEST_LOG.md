# TEST LOG

## 2026-03-25 Red

- 執行指令：`python -m unittest discover -s tests -p "test_*.py" -v`
- 測試總數：15
- 通過數：0
- 失敗數：15（`ERROR`）
- 摘要：先建立 5 題測試與 10 支占位主程式，故所有失敗都來自 `NotImplementedError`，代表測試骨架已正確接上。

## 2026-03-25 Green

- 執行指令：`python -m unittest discover -s tests -p "test_*.py" -v`
- 測試總數：15
- 通過數：15
- 失敗數：0
- 摘要：補上五題最小可行解，包含中位數、罷會模擬、樹狀陣列奇偶查詢、機率公式與密碼候選值統計，全部測試轉綠。

## 2026-03-25 Refactor

- 執行指令：`python -m unittest discover -s tests -p "test_*.py" -v`
- 測試總數：15
- 通過數：15
- 失敗數：0
- 摘要：將簡單版檔名調整為 README 要求的 `-easy.py`，並重構測試載入器支援正式版與簡單版共用驗證，重跑後維持全綠。
