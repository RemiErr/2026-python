# AI_USAGE

## 使用範圍

- 依 `GAME_PLAN/README.md` 與 T01 到 T05 任務文件整理主線需求。
- 協助建立資料檔、核心 API、測試案例與提交文件草稿。
- 協助把需求對應成 `unittest` 驗收項目。

## 人工應理解的內容

- `General`、`BattleConfig`、`Counter`、`defaultdict` 的用途。
- `load_generals()` 與 `load_battles()` 的欄位規則、UTF-8 與 EOF 處理。
- `simulate_battle()` 如何依三波流程更新 `damage`、`losses` 與 `wave_logs`。
- `render_ascii_report()` 為什麼必須只讀不改狀態。

## 使用原則

- AI 只協助產生草稿與整理結構，不應跳過理解與驗證。
- 主線功能以純 Python 為最低提交標準，不依賴 GUI 或 native 模組。
- 最終提交前必須自行重跑測試並確認輸出與文件一致。
