# U3. deque(maxlen=N) 為何能保留最後 N 筆（1.3）
# 說明：deque 是 collections 模組提供的雙向隊列
# 當設定 maxlen 參數時，會自動保留最新的 N 筆資料

from collections import deque

# 建立一個最多容納 3 個元素的隊列
# maxlen=3 表示隊列最大長度只能有 3 個元素
q = deque(maxlen=3)

# 逐一加入 5 個數字（1, 2, 3, 4, 5）
for i in [1, 2, 3, 4, 5]:
    q.append(i)
    # 每次加入元素時，隊列會自動檢查是否超過最大容量
    # 如果超過，最舊的元素會自動被移除

# 最終結果只剩下最後加入的 3 個數字 [3, 4, 5]
# 詳細過程：
# append(1) → [1]
# append(2) → [1, 2]
# append(3) → [1, 2, 3]（滿了）
# append(4) → [2, 3, 4]（1 被移除）
# append(5) → [3, 4, 5]（2 被移除）
