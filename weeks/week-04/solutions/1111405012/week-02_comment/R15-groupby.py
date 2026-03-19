# R15. 分組 groupby（1.15）
# 這個程式示範如何使用 groupby 函數來將資料按照某個鍵值分組

# 匯入 itertools 模組中的 groupby 函數
# groupby 可以將連續相同的元素分組在一起
from itertools import groupby

# 匯入 operator 模組中的 itemgetter 函數
# itemgetter 可以方便地從字典或序列中取出特定位置的值
from operator import itemgetter

# 建立一個列表，其中每個元素都是一個字典（包含日期和地址資訊）
rows = [
    {'date': '07/01/2012', 'address': '...'},
    {'date': '07/02/2012', 'address': '...'}
]

# 重要：根據日期(date)欄位對列表進行排序
# 這是使用 groupby 之前必須要做的步驟，因為 groupby 只能分組連續相同的元素
# itemgetter('date') 表示使用字典中的 'date' 鍵值作為排序的依據
rows.sort(key=itemgetter('date'))

# 使用 groupby 來分組資料
# date: 每一組的日期值（分組的鍵值）
# items: 該日期下所有的資料（可迭代的物件）
for date, items in groupby(rows, key=itemgetter('date')):
    # 遍歷該日期下的每一筆資料
    for i in items:
        # 對每筆資料進行處理（這裡先用 pass，表示不做任何操作）
        pass
