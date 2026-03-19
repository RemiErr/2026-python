# U9. groupby 為何一定要先 sort（1.15）
# 本範例展示在使用 groupby 分組前，為什麼一定要先排序資料

# 從 itertools 模組匯入 groupby（用於分組）
# itertools 裡面有很多與迭代相關的好用工具
from itertools import groupby

# 從 operator 模組匯入 itemgetter（用於取出字典中的值）
# itemgetter 是一個便利工具，比寫 lambda 更簡潔
from operator import itemgetter

# 建立一個包含多個字典的列表，每個字典存放日期和數值
# 注意：這些資料目前「沒有按日期排序」
rows = [
    {'date': '07/02/2012', 'x': 1},  # 第 1 筆：07/02
    {'date': '07/01/2012', 'x': 2},  # 第 2 筆：07/01
    {'date': '07/02/2012', 'x': 3},  # 第 3 筆：07/02（和第 1 筆同日期但不相鄰）
]

# 【錯誤做法】直接使用 groupby，不先排序
# groupby 只會把「連續相同」的元素分在一組
# 在這個例子中：
#   - 第 1 個 07/02 會單獨成一組
#   - 07/01 會成另一組
#   - 第 3 個 07/02 又會成第三組（不會和第 1 個合併）
# 結果：07/02 被分成了兩段，這不是我們想要的
for k, g in groupby(rows, key=itemgetter('date')):
    print(f"日期: {k}, 資料: {list(g)}")  # 07/02 會出現兩次

# 【正確做法】先按日期排序，再使用 groupby
# 排序後的順序：07/01, 07/02, 07/02
# 這樣所有相同日期的資料就會聚在一起
rows.sort(key=itemgetter('date'))

# 現在 groupby 就能正確地分組：
# - 07/01 會成一組
# - 07/02 會成一組（包含原本的第 1 和第 3 筆）
for k, g in groupby(rows, key=itemgetter('date')):
    print(f"日期: {k}, 資料: {list(g)}")  # 07/01 和 07/02 各出現一次
