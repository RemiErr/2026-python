# AI_USAGE

## 我詢問的問題
- 整理 weeks/week-02/HOMEWORK.md 和 weeks/week-02/README.md 的重點要求，
- 要怎麼拆解 Task 1 的輸入輸出與測試案例
- Task 2 的排序寫法和規則排序有什麼需要注意的
- 使用 Collections Counter 要怎麼設計 Task 3 的統計和排序邏輯
- 如何設計空輸入與邊界測試

## 我採用的建議
- 撰寫主要功能並包成函式，方便測試
- 先寫測試案例再回頭完成 main 實作
- Collections 有很多神奇的東西 OvOb
- 官方套件可以解決的問題就不用重複造輪子

## 我拒絕的建議
- 如果直接用 set 輸出會破壞順序
- 純手刻功能

## AI 可能誤導但我修正的案例
- 使用 `most_common(1)` 取得 top action，但同次數時輸出怪怪的。我改成取最大次數後再依字母順序排序。
- 單行手動輸入的話 `sys.stdin.readline()` 比 `sys.stdin.read().strip()` 好用
