# R20. ChainMap 合併映射（1.20）
# ChainMap 用於將多個字典合併成一個「視圖」，查詢時會依序檢查各字典

from collections import ChainMap

# 建立第一個字典 a，包含 x=1 和 z=3
a = {'x': 1, 'z': 3}

# 建立第二個字典 b，包含 y=2 和 z=4
b = {'y': 2, 'z': 4}

# 使用 ChainMap 合併字典 a 和 b
# 重要：a 的優先權比 b 高（先列出的字典優先權更高）
c = ChainMap(a, b)

# 查詢 'x' → 在字典 a 中找到，結果為 1
c['x']

# 查詢 'z' → 在字典 a 中找到，結果為 3
# 雖然字典 b 也有 'z'=4，但因為 a 優先權更高，所以取用 a 的值
c['z']  # 取到 a 的 z 值（3），不是 b 的 z 值（4）
