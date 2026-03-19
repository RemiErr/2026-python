# U7. OrderedDict 的取捨：保序但更吃記憶體（1.7）
# 本範例說明：為什麼 OrderedDict 能記住插入順序，但代價是需要更多的記憶體空間

# 從 collections 模組匯入 OrderedDict（有序字典）
# collections 是 Python 的內建模組，裡面有很多好用的資料結構
from collections import OrderedDict

# 建立一個空的 OrderedDict（有序字典）
# 普通的 dict 在 Python 3.7+ 也會保留插入順序，但 OrderedDict 有額外功能（如 move_to_end）
d = OrderedDict()

# 新增第一個鍵值對：鍵是 'foo'，值是 1
# 順序記錄：第 1 個加入
d['foo'] = 1

# 新增第二個鍵值對：鍵是 'bar'，值是 2
# 順序記錄：第 2 個加入
d['bar'] = 2

# 為什麼 OrderedDict 更吃記憶體？
# - 普通 dict：只存鍵值對
# - OrderedDict：除了存鍵值對，還要額外維持一個「雙向鏈結串列」來記錄插入順序
# 這個額外的結構會占用更多的記憶體空間，但優點是可以保證迭代順序就是插入順序
