# Week 05 解題與測試說明

本目錄依照 `Red → Green → Refactor` 流程完成 5 題程式與單元測試，所有程式都補上繁體中文註解。

## 檔案配置

- `question_10041.py` / `question_10041-easy.py`：Vito's Family 正式版與簡單版
- `question_10050.py` / `question_10050-easy.py`：Hartals 正式版與簡單版
- `question_10055.py` / `question_10055-easy.py`：函數增減性查詢正式版與簡單版
- `question_10056.py` / `question_10056-easy.py`：獲勝機率正式版與簡單版
- `question_10057.py` / `question_10057-easy.py`：密碼候選值正式版與簡單版
- `tests/test_question_*.py`：每題 3 個以上測試案例
- `TEST_LOG.md`：Red、Green、Refactor 三次測試紀錄

## 測試執行方式

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

## 解題重點

- `10041`：排序後取中位數，計算總距離
- `10050`：模擬各政黨罷會日，排除星期五與星期六
- `10055`：以樹狀陣列維護區間內遞減函數數量，奇偶性決定答案
- `10056`：使用等比級數公式計算第 `i` 位玩家獲勝機率
- `10057`：利用中位數區間找出最小值、符合數量與可能個數
