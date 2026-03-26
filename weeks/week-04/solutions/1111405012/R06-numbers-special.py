# R06. 特殊數值：無窮大、NaN、分數、隨機（3.7–3.11）
# 繁體中文註解版：示範數值世界裡較少見但很重要的型別與概念。
# float inf/nan / fractions.Fraction / random

import math
import random
from fractions import Fraction

# ── 3.7 無窮大與 NaN ──────────────────────────────────
a = float("inf")
b = float("-inf")
c = float("nan")
print(a, b, c)  # inf -inf nan
print(math.isinf(a))  # True
print(math.isnan(c))  # True

# 無窮大在某些運算下仍可得到有意義結果。
print(a + 45, 10 / a)  # inf 0.0

# 但未定義運算會得到 nan。
print(a / a, a + b)  # nan nan（未定義）

# NaN 最大的陷阱：它不等於任何值，連自己也不等於自己。
print(c == c)  # False（NaN 不等於自己！）

# ── 3.8 分數運算 ──────────────────────────────────────
p = Fraction(5, 4)
q = Fraction(7, 16)
r = p * q

# Fraction 會保留精確的有理數表示，不會產生 float 誤差。
print(p + q)  # 27/16
print(r.numerator, r.denominator)  # 35 64
print(float(r))  # 0.546875

# limit_denominator() 可以找出近似的簡單分數。
print(r.limit_denominator(8))  # 4/7

# float 也能透過 as_integer_ratio() 轉成 Fraction。
print(Fraction(*(3.75).as_integer_ratio()))  # 15/4

# ── 3.11 隨機選擇 ─────────────────────────────────────
values = [1, 2, 3, 4, 5, 6]
print(random.choice(values))  # 隨機一個
print(random.sample(values, 3))  # 3 個不重複樣本

# shuffle() 會原地修改串列順序。
random.shuffle(values)
print(values)  # 打亂後的序列

print(random.randint(0, 10))  # 0~10 整數

# 設定種子後，隨機序列就可重現，適合測試或教學示範。
random.seed(42)
print(random.random())  # 固定種子：可重現
