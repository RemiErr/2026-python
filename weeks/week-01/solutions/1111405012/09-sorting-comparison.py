# 9 比較、排序與 key 函式範例

# 比較運算(tuple 逐一比較)
# Tuple 比較會從第一個元素開始比較,如果相同才會比較下一個元素
# 這種比較方式稱為「字典序」(lexicographic order)
a = tuple([1, 2])  # 第一個 tuple,包含元素 1 和 2
b = tuple([1, 3])  # 第二個 tuple,包含元素 1 和 3
result = a < b  # 比較過程:先比較第一個元素(1 == 1),再比較第二個元素(2 < 3),結果為 True
print(f"a < b 的結果: {result}")  # 輸出: True

# key 排序
# sorted() 函式可以使用 key 參數指定排序的依據
# lambda 是匿名函式,用來快速定義簡單的函式
rows = [{'uid': 3}, {'uid': 1}, {'uid': 2}]  # 包含三個字典的列表,每個字典有 uid 鍵
rows_sorted = sorted(rows, key=lambda r: r['uid'])  # 根據每個字典的 'uid' 值進行排序
# lambda r: r['uid'] 的意思是:接收參數 r(每個字典),返回 r['uid'] 的值作為排序依據
print(f"排序後的結果: {rows_sorted}")  # 輸出: [{'uid': 1}, {'uid': 2}, {'uid': 3}]

# min/max 搭配 key
# min() 和 max() 函式也可以使用 key 參數來指定比較的依據
smallest = min(rows, key=lambda r: r['uid'])  # 找出 uid 值最小的字典
# 在 rows 列表中,根據 'uid' 的值找出最小的元素
print(f"uid 最小的項目: {smallest}")  # 輸出: {'uid': 1}

# 額外說明:
# 1. 也可以用 max() 找出最大值:largest = max(rows, key=lambda r: r['uid'])
# 2. key 參數接受任何可呼叫的物件(函式),不只是 lambda
# 3. sorted() 會返回新列表,原列表不變;若要原地排序可用 list.sort()
