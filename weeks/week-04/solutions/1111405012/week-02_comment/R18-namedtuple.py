# R18. namedtuple（1.18）
# namedtuple 是一個輕量級的資料結構，用於建立具有名稱欄位的 tuple
# 它比普通的 tuple 更容易閱讀和維護

from collections import namedtuple

# ========== 範例 1: 建立訂閱者資訊 ==========
# 使用 namedtuple 建立 Subscriber 類型
# 參數1: 'Subscriber' 是這個資料型別的名稱
# 參數2: ['email', 'joined'] 是欄位名稱的列表
Subscriber = namedtuple('Subscriber', ['email', 'joined'])

# 建立一個 Subscriber 實例 sub
# 'jonesy@example.com' 對應到 email 欄位
# '2012-10-19' 對應到 joined 欄位
sub = Subscriber('jonesy@example.com', '2012-10-19')

# 使用欄位名稱來存取資料（比起 tuple[0], tuple[1] 更容易理解）
sub.email  # 會回傳 'jonesy@example.com'


# ========== 範例 2: 建立股票資訊並修改 ==========
# 建立 Stock 類型，有三個欄位：名稱、股數、價格
Stock = namedtuple('Stock', ['name', 'shares', 'price'])

# 建立一個 Stock 實例
# name='ACME', shares=100, price=123.45
s = Stock('ACME', 100, 123.45)

# namedtuple 是「不可變」的（immutable），不能直接修改欄位
# 因此使用 _replace() 方法建立一個新的實例，其中 shares 被改為 75
# 原本的 s 保持不變，新的結果被指派回 s
# 現在 s 變成 Stock(name='ACME', shares=75, price=123.45)
s = s._replace(shares=75)
