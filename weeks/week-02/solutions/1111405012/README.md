# Week 02 - 1111405012

## 完成項目
- Task 1：Sequence Clean
- Task 2：Student Ranking
- Task 3：Log Summary

## 執行方式
Python 3.10.6

- Task 1
`python task1_sequence_clean.py`
- Task 2
`python task2_student_ranking.py`
- Task 3
`python task3_log_summary.py`
- Tests
`python -m unittest discover -s tests -p "test_*.py" -v`

## 資料結構選擇理由
- Task 1：用 `list` 保持順序、`set` 記錄已出現元素，`sorted` 產生升降序結果，`list` 篩出偶數。
- Task 2：用 `list` 收集 `(name, score, age)`，再用 `sorted(..., key=...)` 做多條件排序。
- Task 3：用 `Counter` 統計使用者與動作次數，再以排序規則輸出。

## 錯誤與修正方式
- 初始測試因缺少 `task1_sequence_clean.py`、`task2_student_ranking.py`、`task3_log_summary.py` 而失敗（ImportError），補上實作與 `main()` 後恢復全綠。

## Red → Green → Refactor 摘要
- Task 1
Red：測試模組載入失敗。
Green：實作 `process_numbers` 與輸出格式。
Refactor：抽出 `dedupe_preserve` 與 `format_line`，使邏輯清楚可重用。

- Task 2
Red：測試模組載入失敗。
Green：加入 `sort_students` 與 `top_k`，完成排序邏輯。
Refactor：將排序規則集中在 `sort_students`，主程式只負責輸入輸出。

- Task 3
Red：測試模組載入失敗。
Green：使用 `Counter` 完成使用者與動作統計。
Refactor：補上 top action 同次數時的字母序決定，避免不確定輸出。
