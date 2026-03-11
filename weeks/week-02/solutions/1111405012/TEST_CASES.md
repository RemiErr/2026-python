# TEST_CASES

## Case 1 - Task 1 Normal
Input:
```
5 3 5 2 9 2 8 3 1
```
Expected Output:
```
dedupe: 5 3 2 9 8 1
asc: 1 2 2 3 3 5 5 8 9
desc: 9 8 5 5 3 3 2 2 1
evens: 2 2 8
```
Actual Output:
```
dedupe: 5 3 2 9 8 1
asc: 1 2 2 3 3 5 5 8 9
desc: 9 8 5 5 3 3 2 2 1
evens: 2 2 8
```
Result: PASS
Test: `tests/test_task1.py::test_dedupe_preserves_order`
Fix: 補上去重與排序的實作後通過。

## Case 2 - Task 1 Edge (Empty)
Input:
```

```
Expected Output:
```
dedupe:
asc:
desc:
evens:
```
Actual Output:
```
dedupe:
asc:
desc:
evens:
```
Result: PASS
Test: `tests/test_task1.py::test_empty_input`
Fix: 空輸入時使用空陣列並輸出只有標籤。

## Case 3 - Task 2 Tie Break
Input:
```
3 3
bob 88 19
amy 88 19
zoe 88 19
```
Expected Output:
```
amy 88 19
bob 88 19
zoe 88 19
```
Actual Output:
```
amy 88 19
bob 88 19
zoe 88 19
```
Result: PASS
Test: `tests/test_task2.py::test_tie_break_by_name`
Fix: 排序 key 改為 (-score, age, name)。

## Case 4 - Task 3 Normal
Input:
```
8
alice login
bob login
alice view
alice logout
bob view
bob view
chris login
bob logout
```
Expected Output:
```
bob 4
alice 3
chris 1
top_action: login 3
```
Actual Output:
```
bob 4
alice 3
chris 1
top_action: login 3
```
Result: PASS
Test: `tests/test_task3.py::test_summary_counts`
Fix: 使用 `Counter` 統計並依規則排序。

## Case 5 - Task 3 Edge (Empty m)
Input:
```
0
```
Expected Output:
```
top_action: None 0
```
Actual Output:
```
top_action: None 0
```
Result: PASS
Test: `tests/test_task3.py::test_empty_input`
Fix: m=0 時仍輸出 top_action 的預設值。
