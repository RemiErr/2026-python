# U6. defaultdict 為何比手動初始化乾淨（1.6）
# 這個程式展示了 defaultdict 如何簡化字典操作

from collections import defaultdict

# 建立一個包含重複鍵的列表，每個元素是 (鍵, 值) 的元組
pairs = [('a', 1), ('a', 2), ('b', 3)]

# ============== 方法 1：手動版（傳統做法） ==============
# 建立一個空字典
d = {}

# 逐個處理 pairs 中的每一個 (鍵, 值) 對
for k, v in pairs:
    # 檢查這個鍵是否已經存在於字典中
    if k not in d:
        # 如果鍵不存在，就建立一個新的空列表作為值
        d[k] = []
    # 不管鍵是新的或已存在，都把數值 v 加到列表裡面
    d[k].append(v)

# 手動版的結果：d = {'a': [1, 2], 'b': [3]}
# ❌ 缺點：程式碼很繁瑣，每次都要判斷鍵是否存在

# ============== 方法 2：defaultdict（聰明做法） ==============
# 建立一個 defaultdict，預設值為 list（空列表）
# 當存取一個不存在的鍵時，會自動建立空列表
d2 = defaultdict(list)

# 逐個處理 pairs 中的每一個 (鍵, 值) 對
for k, v in pairs:
    # 直接把 v 加到 d2[k] 的列表裡
    # 如果鍵不存在，defaultdict 會自動建立一個空列表
    d2[k].append(v)

# defaultdict 版的結果：d2 = defaultdict(list, {'a': [1, 2], 'b': [3]})
# ✅ 優點：程式碼簡潔，不需要重複的 if 判斷
