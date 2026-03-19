# R17. 字典子集（1.17）
# 主題：使用字典推導式篩選字典中的項目

# 建立一個字典，儲存公司名稱（鍵）和對應的股票價格（值）
prices = {'ACME': 45.23, 'AAPL': 612.78, 'IBM': 205.55}

# 方法1：根據「值」篩選 - 建立新字典，只包含股票價格 > 200 的公司
# 使用字典推導式：遍歷 prices.items()，只保留滿足條件 (v > 200) 的項目
p1 = {k: v for k, v in prices.items() if v > 200}
# 結果：{'AAPL': 612.78, 'IBM': 205.55}

# 建立一個集合，儲存指定的科技公司名稱
tech_names = {'AAPL', 'IBM'}

# 方法2：根據「鍵」篩選 - 建立新字典，只包含在 tech_names 中的公司
# 使用字典推導式：遍歷 prices.items()，只保留鍵在 tech_names 集合內的項目
p2 = {k: v for k, v in prices.items() if k in tech_names}
# 結果：{'AAPL': 612.78, 'IBM': 205.55}
