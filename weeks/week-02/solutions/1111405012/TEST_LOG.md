# TEST_LOG

## Run 1 (Red) - 2026-03-11
Command:
`python -m unittest discover -s tests -p "test_*.py" -v`
Summary: total 3, passed 0, failed 0, errors 3
Notes: 測試載入時出現 ModuleNotFoundError，因三個任務檔案尚未建立。

## Run 2 (Green) - 2026-03-11
Command:
`python -m unittest discover -s tests -p "test_*.py" -v`
Summary: total 9, passed 9, failed 0, errors 0
Notes: 新增三個任務程式並整理為可重用函式，測試全部通過。
