# R11. 命名切片 slice（1.11）

# 用 slice 物件替切片「命名」，可重複使用也更容易閱讀
record = "....................100 .......513.25 .........."
SHARES = slice(20, 23)  # [20:23] 對應股數字串
PRICE = slice(31, 37)   # [31:37] 對應價格字串

# 讀取子字串後再轉成數值做運算
cost = int(record[SHARES]) * float(record[PRICE])
