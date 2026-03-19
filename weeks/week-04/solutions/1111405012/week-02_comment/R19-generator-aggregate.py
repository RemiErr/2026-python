# R19. 轉換+聚合：生成器表達式（1.19）

# ===== 範例 1：計算平方和 =====
nums = [1, 2, 3]
# sum() 是聚合函數，(x * x for x in nums) 是生成器表達式
# 生成器表達式會逐一產生每個 x 的平方值，sum() 再將它們加起來
# 計算：1*1 + 2*2 + 3*3 = 1 + 4 + 9 = 14
sum(x * x for x in nums)

# ===== 範例 2：將元組元素轉換為字串並用逗號連接 =====
s = ('ACME', 50, 123.45)
# ','.join() 是字串合併函數
# (str(x) for x in s) 是生成器表達式，會將元組中的每個元素轉換為字串
# join() 再將它們用逗號連接起來
# 結果：'ACME,50,123.45'
','.join(str(x) for x in s)

# ===== 範例 3：從投資組合中找出最少的股票數量 =====
portfolio = [{'name': 'AOL', 'shares': 20}, {'name': 'YHOO', 'shares': 75}]
# min() 是聚合函數，用來找最小值
# (s['shares'] for s in portfolio) 是生成器表達式
# 從每個字典中取出 'shares' 的值，然後找出最小值
# 結果：20（因為 AOL 有 20 股，YHOO 有 75 股）
min(s['shares'] for s in portfolio)

# ===== 範例 4：從投資組合中找出股票數量最少的項目 =====
# min() 加上 key 參數，用來指定比較的標準
# key=lambda s: s['shares'] 表示：根據字典中的 'shares' 值來比較
# 結果：{'name': 'AOL', 'shares': 20}（整個字典物件）
min(portfolio, key=lambda s: s['shares'])
