# R1. 序列解包（1.1）

# 1. 序列（tuple/list）可以直接拆成多個變數
p = (4, 5)
# 這行會依序把 p[0], p[1] 指派給 x, y
x, y = p

# 2. 解包也可以用在 list，且元素可以是巢狀序列
data = ["ACME", 50, 91.1, (2012, 12, 21)]
# 這裡第四個元素 (2012, 12, 21) 先整包給 date
name, shares, price, date = data
# 也可以在解包時「往更深一層」解出年/月/日
name, shares, price, (year, mon, day) = data

# 3. 丟棄不需要的值：用底線作為占位（慣例）
_, shares, price, _ = data
