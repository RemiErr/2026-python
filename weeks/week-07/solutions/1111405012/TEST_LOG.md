# 赤壁戰役測試日誌

## RED

- 初始狀態只有 `GAME_PLAN/` 規格文件，主線交付物尚未建立。
- 在這個狀態下執行測試會因為缺少 `chibi_battle.py`、資料檔與測試檔而失敗。

## GREEN

- 建立 `weeks/week-07/generals.txt` 與 `weeks/week-07/battles.txt`，並在 solution 目錄保留同內容副本。
- 完成 `chibi_battle.py`：資料模型、UTF-8/EOF 讀檔、欄位驗證、三波模擬、傷害排行、勢力統計、戰敗判定。
- 完成 `chibi_battle_easy.py`：直接進入可遊玩的文字 CLI 模式。
- 完成 `test_chibi.py`：涵蓋 I/O、EOF、驗證、排序、最低傷害、三波模擬、互動流程、排行、勢力統計、戰敗判定、報表唯讀。

## REFACTOR

- 將資料解析拆成模組層函式 `load_generals()` 與 `load_battles()`，讓測試與 CLI 都能共用。
- 將戰鬥狀態重置集中在 `reset_battle_state()`，避免重跑模擬時殘留舊狀態。
- 以 `render_ascii_report()` 只讀取當前統計資料，並用測試驗證報表產生前後狀態不變。
- 新增 `play_wave()` 與 `play_game()`，讓盟軍回合可由玩家指定攻擊目標，同時保留原本自動模擬 API。

## 測試指令

```powershell
python -m unittest discover -s weeks/week-07/solutions/1111405012 -p test_chibi.py -v
```

## 最終結果

- 已執行：

```powershell
python -m unittest discover -s weeks/week-07/solutions/1111405012 -p test_chibi.py -v
```

- 測試摘要：

```text
Ran 19 tests in 0.069s
OK
```

- CLI 額外檢查：

```powershell
python weeks/week-07/solutions/1111405012/chibi_battle.py
```

- CLI 成功輸出三波摘要、傷害排行、勢力統計與戰敗名單。
