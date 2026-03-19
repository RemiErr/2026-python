# R16. 過濾：推導式 / generator / filter / compress（1.16）

# ========== 方法1：列表推導式 (List Comprehension) ==========
# 用途：快速創建一個新列表，只包含符合條件的元素
from itertools import compress
mylist = [1, 4, -5, 10]
# 這行代碼會過濾出 mylist 中所有大於 0 的數字，並創建一個新列表
# 結果：[1, 4, 10]
[n for n in mylist if n > 0]

# ========== 方法2：生成器表達式 (Generator Expression) ==========
# 用途：類似列表推導式，但更省記憶體（不會一次性存儲所有結果）
# 生成器會在需要時才計算每個值
pos = (n for n in mylist if n > 0)
# 這個生成器可以逐個產生符合條件的數字

# ========== 方法3：filter() 函數 ==========
# 用途：使用一個函數來判斷每個元素是否符合條件

values = ['1', '2', '-3', '-', 'N/A']

# 定義一個判斷函數：檢查字串是否能轉換成整數


def is_int(val):
    try:
        # 嘗試將字串轉換成整數
        int(val)
        # 如果成功，回傳 True
        return True
    except ValueError:
        # 如果轉換失敗（拋出異常），表示不是整數，回傳 False
        return False


# 用 filter() 函數過濾 values 列表
# filter() 會對每個元素呼叫 is_int() 函數，只保留回傳 True 的元素
# 結果：['1', '2']（只有能轉換成整數的字串）
list(filter(is_int, values))

# ========== 方法4：compress() 函數 ==========
# 用途：根據一個布林值列表來過濾另一個列表

addresses = ['a1', 'a2', 'a3']  # 地址列表
counts = [0, 3, 10]  # 計數列表

# 創建一個布林值列表，判斷每個計數是否大於 5
# 結果：[False, False, True]
# 0 > 5 → False
# 3 > 5 → False
# 10 > 5 → True
more5 = [n > 5 for n in counts]

# 使用 compress() 函數，根據 more5 布林列表來過濾 addresses
# 只保留對應位置布林值為 True 的地址
# 結果：['a3']（因為只有第3個計數大於5）
list(compress(addresses, more5))
