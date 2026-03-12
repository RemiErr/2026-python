# R3. deque 保留最後 N 筆（1.3）

# deque：雙端佇列，可在兩端快速 push/pop
from collections import deque

# 1. 設定 maxlen，超出時會自動丟掉「最舊」的一端
q = deque(maxlen=3)
q.append(1); q.append(2); q.append(3)
# 這時內容是 [1, 2, 3]，再塞 4 會把 1 擠掉
q.append(4)  # 自動丟掉最舊的 1

# 2. 不設 maxlen 就是一般雙端佇列
q = deque()
# append 從右邊加，appendleft 從左邊加
q.append(1); q.appendleft(2)
# pop 從右邊拿，popleft 從左邊拿
q.pop(); q.popleft()
