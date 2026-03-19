# U2. 星號解包為何能處理「不定長」且結果固定是 list（1.2）

# ============ 程式說明 ============
# 這個程式示範了 Python 中的「星號解包」（star unpacking）
# 星號解包能夠自動將多個值捆綁在一起，形成一個 list
# 即使沒有剩餘的值，結果仍然是一個空的 list

# 建立一個包含 2 個元素的 tuple（元組）
# tuple 是一種不可變的序列，用括號表示
record = ('Dave', 'dave@example.com')

# 使用星號解包：name, email, *phones = record
# 說明：
#   - name：接收第 1 個值 'Dave'
#   - email：接收第 2 個值 'dave@example.com'
#   - *phones：用星號 (*) 接收「剩餘所有的值」
#             這裡沒有剩餘的值，所以 phones = []（空 list）
#             注意：即使沒有值，*phones 也一定是 list 類型
name, email, *phones = record

# phones == []  ✓ 驗證：phones 確實是一個空 list，不是 None 或其他類型
