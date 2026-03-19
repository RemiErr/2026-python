# U10. zip 為何只能用一次（1.8）
# 本範例展示迭代器（iterator）的重要特性：一旦被消耗，就無法再使用

# 建立一個字典：存放商品名稱和價格
prices = {'A': 2.0, 'B': 1.0}

# 使用 zip() 建立一個迭代器
# zip() 回傳的是一個「迭代器」，不是列表
# 迭代器的特點：它可以被遍歷一次，但一旦遍歷完，就沒有了
z = zip(prices.values(), prices.keys())

# 第一次使用：找最小值
# min(z) 會逐個取出 z 中的元素，直到找到最小值
# 這個過程中，迭代器 z 被「消耗」了
min(z)  # 結果：(1.0, 'B')，成功

# 第二次使用：找最大值
# 但是！z 已經被 min(z) 消耗完了，沒有元素可以用了
# 所以這行會回傳 ValueError（因為 max() 無法在空的迭代器上操作）
max(z)  # ❌ 會失敗！迭代器已經被用完了

# 【如何修正】如果你需要多次使用相同的資料，有幾種方法：
# 方法 1：把迭代器轉換成列表（會占用較多記憶體，但可以多次使用）
z_list = list(zip(prices.values(), prices.keys()))
min(z_list)  # ✅ OK
max(z_list)  # ✅ OK

# 方法 2：建立多個迭代器
z1 = zip(prices.values(), prices.keys())
z2 = zip(prices.values(), prices.keys())
min(z1)  # ✅ OK
max(z2)  # ✅ OK
