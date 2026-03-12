# R4. heapq 取 Top-N（1.4）

# heapq：以「最小值」為根的堆積結構（min-heap）
import heapq

nums = [1, 8, 2, 23, 7, -4, 18, 23, 42, 37, 2]
# 1. 直接取最大/最小的前 N 個
heapq.nlargest(3, nums)
heapq.nsmallest(3, nums)

# 2. 對複雜結構可提供 key
portfolio = [
    {"name": "IBM", "shares": 100, "price": 91.1},
    {"name": "AAPL", "shares": 50, "price": 543.22},
]
# 依 price 找最小的一筆
heapq.nsmallest(1, portfolio, key=lambda s: s["price"])

# 3. 把 list 轉成 heap 後，用 heappop 取最小值
heap = list(nums)
heapq.heapify(heap)
heapq.heappop(heap)
