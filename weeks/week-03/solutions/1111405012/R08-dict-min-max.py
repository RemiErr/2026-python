# R8. 字典運算：min/max/sorted + zip（1.8）

prices = {"ACME": 45.23, "AAPL": 612.78, "FB": 10.75}

# 1. zip(values, keys) 會產生 (value, key) 的序列
#    這樣用 min/max/sorted 就能依 value 排序
min(zip(prices.values(), prices.keys()))
max(zip(prices.values(), prices.keys()))
sorted(zip(prices.values(), prices.keys()))

# 2. 也可以直接對 key 做 min/max，搭配 key= 依 value 比較
min(prices, key=lambda k: prices[k])  # 回傳 key（最小 value 對應的 key）
