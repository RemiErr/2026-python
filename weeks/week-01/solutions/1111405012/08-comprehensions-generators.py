# 8 容器操作與推導式範例

# === 1. 列表推導式 (List Comprehension) ===
# 列表推導式是一種簡潔的方式來建立新列表
# 語法: [表達式 for 變數 in 可迭代物件 if 條件]
nums = [1, -2, 3, -4]

# 使用列表推導式過濾出正數
# 這行程式碼的意思是:「從 nums 中取出每個數字 n,如果 n > 0 就放入新列表」
positives = [n for n in nums if n > 0]

print(positives)  # Output: [1, 3]
# 等同於傳統寫法:
# positives = []
# for n in nums:
#     if n > 0:
#         positives.append(n)

# === 2. 字典推導式 (Dictionary Comprehension) ===
# 字典推導式可以快速建立字典
# 語法: {鍵表達式: 值表達式 for 變數 in 可迭代物件}
pairs = [('a', 1), ('b', 2)]

# 將 tuple 配對列表轉換為字典
# k 代表 key (鍵), v 代表 value (值)
lookup = {k: v for k, v in pairs}

print(lookup)  # Output: {'a': 1, 'b': 2}
# 等同於傳統寫法:
# lookup = {}
# for k, v in pairs:
#     lookup[k] = v

# === 3. 生成器表達式 (Generator Expression) ===
# 生成器表達式類似列表推導式,但使用小括號 () 而非中括號 []
# 優點: 不會一次產生所有元素,節省記憶體空間
# 計算所有數字的平方和
squares_sum = sum(n * n for n in nums)
# 這會產生: 1² + (-2)² + 3² + (-4)² = 1 + 4 + 9 + 16 = 30

print(squares_sum)  # Output: 30
# 注意: 生成器表達式是「惰性求值」(lazy evaluation)
# 只有在需要時才計算下一個值,適合處理大量資料
