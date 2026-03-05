# 10 模組、類別、例外與 Big-O（最低門檻）範例

# === 1. 模組導入 ===
# collections 是 Python 內建的集合模組，提供許多特殊的容器型別
from collections import deque  # 導入 deque（雙端佇列）資料結構

# === 2. deque 雙端佇列使用 ===
# deque 是一種可以從兩端快速新增/刪除元素的資料結構
# maxlen=2 表示這個佇列最多只能存放 2 個元素
q = deque(maxlen=2)  # 建立一個最大容量為 2 的雙端佇列
q.append(1)  # 加入元素 1，此時 q = deque([1])
q.append(2)  # 加入元素 2，此時 q = deque([1, 2])
q.append(3)  # 自動丟掉最舊，加入元素 3 時，最舊的 1 會被自動移除，此時 q = deque([2, 3])
# deque 會自動維持最多 2 個元素，常用於實現固定大小的緩衝區或歷史記錄

# === 3. 類別定義 ===
# class 是物件導向程式設計的核心，用來定義自訂的資料型別


class User:
    # __init__ 是建構子（constructor），在建立物件時自動呼叫
    # self 代表物件本身，類似其他語言的 this
    # user_id 是初始化時需要傳入的參數
    def __init__(self, user_id):
        # self.user_id 是物件的屬性（attribute），儲存使用者的 ID
        self.user_id = user_id  # 將傳入的 user_id 儲存到物件屬性中


# === 4. 物件實例化與屬性存取 ===
u = User(42)  # 建立一個 User 物件，傳入 user_id = 42
uid = u.user_id  # 透過「物件.屬性名稱」來存取物件的屬性，此時 uid = 42

# 例外處理
# === 5. try-except 例外處理機制 ===
# 例外處理用來捕捉程式執行時可能發生的錯誤，避免程式崩潰


def is_int(val):
    """
    檢查一個值是否可以轉換為整數

    參數:
        val: 任意型別的值

    返回:
        True 如果可以轉換為整數，否則返回 False
    """
    try:
        # try 區塊內放可能會產生錯誤的程式碼
        int(val)  # 嘗試將 val 轉換為整數
        return True  # 如果轉換成功，返回 True
    except ValueError:
        # except 區塊用來捕捉特定類型的例外
        # ValueError 會在 int() 無法轉換時產生（例如 int("abc")）
        return False  # 如果轉換失敗，返回 False

# 使用範例:
# is_int("123")   -> True（字串 "123" 可以轉換為整數）
# is_int("abc")   -> False（字串 "abc" 無法轉換為整數）
# is_int(45.7)    -> True（浮點數會被截斷為整數）

# Big-O 只是觀念提示
# === 6. 時間複雜度 Big-O 概念 ===
# Big-O 表示法用來描述演算法執行時間如何隨輸入大小增長
# O(1) 表示常數時間：無論資料量多大，執行時間都固定
# O(N) 表示線性時間：執行時間與資料量成正比

# list.append 通常是 O(1)
# append() 在串列尾端加入元素，通常只需固定時間（偶爾需要擴充記憶體時會是 O(N)，但平均是 O(1)）
# 範例: my_list.append(5) 無論 my_list 有多長，append 都很快

# list 切片是 O(N)
# 切片操作需要複製元素，所需時間與切片長度成正比
# 範例: my_list[10:1000] 會複製 990 個元素，所以是 O(990) = O(N)

# === 額外補充 ===
# 常見的時間複雜度排序（從快到慢）：
# O(1) < O(log N) < O(N) < O(N log N) < O(N²) < O(2^N) < O(N!)
# 範例:
# - 字典查詢: O(1)
# - 二分搜尋: O(log N)
# - 線性搜尋: O(N)
# - 排序演算法: O(N log N)
# - 巢狀迴圈: O(N²)

# === 7. 執行結果展示 ===
print("=== deque 雙端佇列示範 ===")
print(f"當前 deque 內容: {q}")  # 顯示 deque([2, 3])
print(f"deque 的最大長度: {q.maxlen}")

print("\n=== 類別與物件示範 ===")
print(f"使用者 ID: {uid}")  # 顯示 42
print(f"使用者物件: {u}")  # 顯示物件資訊
print(f"物件類型: {type(u)}")  # 顯示 <class '__main__.User'>

print("\n=== 例外處理示範 ===")
test_values = ["123", "abc", 45.7, "3.14", None]
for val in test_values:
    result = is_int(val)
    print(f"is_int({repr(val):>10}) -> {result}")

print("\n=== Big-O 時間複雜度示範 ===")
demo_list = list(range(10))  # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
print(f"原始串列: {demo_list}")

# O(1) 操作 - append
demo_list.append(10)
print(f"append(10) 後: {demo_list}  # O(1) 操作")

# O(N) 操作 - 切片
sliced = demo_list[2:7]
print(f"切片 [2:7]: {sliced}  # O(N) 操作，N = 切片長度")
