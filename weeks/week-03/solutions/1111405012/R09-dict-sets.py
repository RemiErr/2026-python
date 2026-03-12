# R9. 兩字典相同點：keys/items 集合運算（1.9）

a = {"x": 1, "y": 2, "z": 3}
b = {"w": 10, "x": 11, "y": 2}

# 1. keys() / items() 都是「可做集合運算」的 view
a.keys() & b.keys()   # 交集：兩者都有的 key
a.keys() - b.keys()   # 差集：只在 a 裡的 key
a.items() & b.items() # (key, value) 完全相同的項目

# 2. 用集合運算結果來過濾字典
c = {k: a[k] for k in a.keys() - {"z", "w"}}
