# R7. OrderedDict（1.7）

# OrderedDict 會保留插入順序（Python 3.7+ 一般 dict 也會）
from collections import OrderedDict
import json

d = OrderedDict()
d["foo"] = 1; d["bar"] = 2
# 轉成 JSON 會依插入順序輸出
json.dumps(d)
