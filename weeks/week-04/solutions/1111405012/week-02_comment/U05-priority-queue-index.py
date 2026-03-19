# U5. 優先佇列為何要加 index（1.5）
# 重點：當優先級相同時，Python 會自動比較下一個元素，這會導致問題

import heapq

# ============= 定義一個簡單的物品類別 =============


class Item:
    """
    這是一個簡單的類別，代表優先佇列中的一個物品
    每個物品都有一個名字（例如 'a', 'b'）
    """

    def __init__(self, name):
        self.name = name


# ============= 問題：沒有加 index 會發生什麼？ =============
pq = []

# ❌ 這個方法會出錯（已被註解掉）：
# 當你只放 (priority, item) 這樣的二元組時：
#   - heapq 是最小堆（優先級越小越先出來）
#   - 如果兩個元素的 priority 相同，heapq 會自動比較第二個元素 (item)
#   - 但 Item 類別沒有定義 < 運算子（比較大小的方法）
#   - 所以 Python 不知道怎麼比較兩個 Item，會拋出 TypeError
#
# heapq.heappush(pq, (-1, Item('a')))
# heapq.heappush(pq, (-1, Item('b')))  # ❌ TypeError: '<' not supported between instances of 'Item' and 'Item'

# ============= 解決方案：加入 index 作為第二個元素 =============
# 透過加入一個遞增的 index，我們可以確保：
#   1. 當 priority 相同時，heapq 會比較 index（數字）而不是 Item 物件
#   2. 數字可以直接比較大小，所以不會出錯
#   3. index 會按照加入的順序遞增，就像 FIFO（先進先出）
#   4. 這樣做的副作用是：同優先級的元素會按照加入順序出來

idx = 0
# 加入第一個物品：優先級 -1，index 0，物品名稱 'a'
heapq.heappush(pq, (-1, idx, Item('a')))
idx += 1

# 加入第二個物品：優先級 -1，index 1，物品名稱 'b'
heapq.heappush(pq, (-1, idx, Item('b')))
idx += 1

# 現在 pq 看起來像：[(-1, 0, Item('a')), (-1, 1, Item('b'))]
# 如果你 heappop，會先拿到 (-1, 0, Item('a'))
