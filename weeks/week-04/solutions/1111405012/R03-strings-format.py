# R03. 字串清理、對齊、拼接與格式化（2.11–2.16）
# 本程式展示 Python 中字串處理的六大重要技巧

# 導入 textwrap 模組，用來處理長字串的換行和縮排
import textwrap

# ═══════════════════════════════════════════════════════════════
# ── 2.11 清理字元（移除前後多餘的空白或符號）─────────────────
# ═══════════════════════════════════════════════════════════════

# 建立一個包含前後空白和換行符號的字串
s = "  hello world \n"

# .strip() = 移除字串「兩端」的空白（左邊和右邊都移除）
# repr() 是用來顯示字串的真實樣子（包括隱藏的空白和換行符 \n）
print(repr(s.strip()))  # 輸出: 'hello world'（前後空白都被移除了）

# .lstrip() = 只移除字串「左邊」的空白
print(repr(s.lstrip()))  # 輸出: 'hello world \n'（右邊的換行符仍保留）

# .strip("-=") = 移除字串兩端指定的符號（這裡移除 "-" 和 "=" 符號）
print("-----hello=====".strip("-="))  # 輸出: 'hello'（前後的 - 和 = 都被移除）

# ═══════════════════════════════════════════════════════════════
# ── 2.13 字串對齊（在固定寬度內排列字串）───────────────────────
# ═══════════════════════════════════════════════════════════════

# 定義一個基礎字串
text = "Hello World"

# .ljust(20) = 左對齊，將字串填充到 20 個字元的寬度（右邊用空白填滿）
print(text.ljust(20))  # 輸出: 'Hello World         '（右邊有 9 個空白）

# .rjust(20) = 右對齊，將字串填充到 20 個字元的寬度（左邊用空白填滿）
print(text.rjust(20))  # 輸出: '         Hello World'（左邊有 9 個空白）

# .center(20, "*") = 置中對齊，用星號 "*" 作為填充字符
print(text.center(20, "*"))  # 輸出: '****Hello World*****'（兩邊用星號填滿）

# format(text, "^20") = 也是置中對齊的另一種寫法（^ 表示置中）
print(format(text, "^20"))  # 輸出: '    Hello World     '（兩邊用空白填滿）

# format(1.2345, ">10.2f") = 右對齊數字，保留 2 位小數點，寬度 10 個字元
# > 表示右對齊，10 是總寬度，.2f 是保留 2 位小數
print(format(1.2345, ">10.2f"))  # 輸出: '      1.23'（四捨五入到 2 位小數，左邊補空白）

# ═══════════════════════════════════════════════════════════════
# ── 2.14 合併拼接（把多個字串連接成一個）──────────────────────
# ═══════════════════════════════════════════════════════════════

# 定義一個字串列表（清單），包含 4 個單詞
parts = ["Is", "Chicago", "Not", "Chicago?"]

# " ".join(parts) = 用「空白」作為分隔符號，把列表中的所有字串連接起來
print(" ".join(parts))  # 輸出: 'Is Chicago Not Chicago?'（用空白分隔）

# ",".join(parts) = 用「逗號」作為分隔符號，把列表中的所有字串連接起來
print(",".join(parts))  # 輸出: 'Is,Chicago,Not,Chicago?'（用逗號分隔，適合 CSV 格式）

# 定義一個混合型列表，包含字串和數字
data = ["ACME", 50, 91.1]

# str(d) for d in data = 把列表中的每一項都轉換成字串（因為數字無法直接用 join）
# 然後用逗號連接所有項目
print(",".join(str(d) for d in data))  # 輸出: 'ACME,50,91.1'

# ═══════════════════════════════════════════════════════════════
# ── 2.15 插入變量（把變量的值嵌入到字串中）────────────────────
# ═══════════════════════════════════════════════════════════════

# 定義兩個變量：一個字串和一個數字
name, n = "Guido", 37

# 定義一個模板字串，用 {name} 和 {n} 作為占位符（待填空）
s = "{name} has {n} messages."

# 方法 1：使用 .format(name=name, n=n) 填充占位符
# name=name 表示把第一個 {name} 替換成變量 name 的值
# n=n 表示把 {n} 替換成變量 n 的值
print(s.format(name=name, n=n))  # 輸出: 'Guido has 37 messages.'

# 方法 2：使用 .format_map(vars()) 填充占位符
# vars() 會把所有現在的變量轉成一個字典（即 {'name': 'Guido', 'n': 37}）
# format_map 會自動從字典中找到相對應的值
print(s.format_map(vars()))  # 輸出: 'Guido has 37 messages.'

# 方法 3：使用 f-string（f"..." 語法）- 最簡潔最現代的方法
# 直接在字串中用 {變量名} 就能插入變量的值
print(f"{name} has {n} messages.")  # 輸出: 'Guido has 37 messages.'

# ═══════════════════════════════════════════════════════════════
# ── 2.16 指定列寬（把長字串自動斷行到指定寬度）──────────────────
# ═══════════════════════════════════════════════════════════════

# 定義一個很長的句子（用括號和多行字串來方便閱讀）
long_s = (
    "Look into my eyes, look into my eyes, the eyes, "
    "not around the eyes, look into my eyes, you're under."
)

# textwrap.fill(long_s, 40) = 把長字串自動換行，每行最多 40 個字元
print(textwrap.fill(long_s, 40))
# 輸出類似：
# Look into my eyes, look into my
# eyes, the eyes, not around the
# eyes, look into my eyes, you're under.

# textwrap.fill(long_s, 40, initial_indent="    ") = 同上，但第一行前面加 4 個空白（縮排）
print(textwrap.fill(long_s, 40, initial_indent="    "))
# 輸出類似：
#     Look into my eyes, look into my
# eyes, the eyes, not around the
# eyes, look into my eyes, you're under.
