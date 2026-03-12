# R6. 多值字典 defaultdict / setdefault（1.6）

# defaultdict 會在 key 不存在時，自動建立預設容器
from collections import defaultdict

# 1. 用 list 蒐集多個值
d = defaultdict(list)
d["a"].append(1); d["a"].append(2)

# 2. 用 set 蒐集且去重
d = defaultdict(set)
d["a"].add(1); d["a"].add(2)

# 3. 不用 defaultdict 的寫法：setdefault 會回傳預設值
d = {}
d.setdefault("a", []).append(1)
