# R2. 解包數量不固定：星號解包（1.2）

# 1. * 可以吃掉「不固定長度」的中間或前段/後段
def drop_first_last(grades):
    # first 取第一個，last 取最後一個，中間全部交給 middle
    first, *middle, last = grades
    # 只算中間分數的平均
    return sum(middle) / len(middle)

# 2. * 也能用在字串/通訊錄資料
record = ("Dave", "dave@example.com", "773-555-1212", "847-555-1212")
# phone_numbers 會是一個 list，收集剩下的電話
name, email, *phone_numbers = record

# 3. * 放在前面：尾端保留 current，前面的都塞進 trailing
*trailing, current = [10, 8, 7, 1, 9, 5, 10, 3]
