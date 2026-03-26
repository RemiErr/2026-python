# R05. 數字基礎：四捨五入、進制、格式化（3.1–3.4）
# 繁體中文註解版：涵蓋 float、Decimal 與數值格式化基礎。
# round / Decimal / format / bin / oct / hex

from decimal import Decimal, localcontext
import math

# ── 3.1 四捨五入 ──────────────────────────────────────
print(round(1.27, 1))  # 1.3
print(round(1.25361, 3))  # 1.254

# Python 的 round() 採用銀行家捨入（五取偶）。
print(round(0.5))  # 0（銀行家捨入，取最近偶數）
print(round(2.5))  # 2

a = 1627731

# 第二個參數若為負數，代表往十位、百位、千位做四捨五入。
print(round(a, -2))  # 1627700（對百位四捨五入）

# ── 3.2 精確浮點數 ────────────────────────────────────
# 一般 float 採二進位浮點表示，部分十進位小數無法精準表示。
print(4.2 + 2.1)  # 6.300000000000001（有誤差）

# Decimal 以十進位為核心，適合需要精確小數的場景。
da, db = Decimal("4.2"), Decimal("2.1")
print(da + db)  # 6.3（精確）

# localcontext() 可暫時調整 Decimal 計算精度。
with localcontext() as ctx:
    ctx.prec = 3
    print(Decimal("1.3") / Decimal("1.7"))  # 0.765

# math.fsum() 對大量浮點數求和更穩定。
print(math.fsum([1.23e18, 1, -1.23e18]))  # 1.0（正確）

# ── 3.3 數字格式化 ────────────────────────────────────
x = 1234.56789
print(format(x, "0.2f"))  # '1234.57'
print(format(x, ">10.1f"))  # '    1234.6'
print(format(x, ","))  # '1,234.56789'
print(format(x, "0,.2f"))  # '1,234.57'
print(format(x, "e"))  # '1.234568e+03'

# ── 3.4 二八十六進制 ──────────────────────────────────
n = 1234
print(bin(n), oct(n), hex(n))  # 0b10011010010 0o2322 0x4d2

# format() 可以輸出不帶 0b / 0o / 0x 前綴的版本。
print(format(n, "b"), format(n, "x"))  # 10011010010 4d2

# int() 也能把不同進位的字串還原成十進位整數。
print(int("4d2", 16), int("2322", 8))  # 1234 1234
