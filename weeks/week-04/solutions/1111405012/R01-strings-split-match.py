# R01. 字串分割與匹配（2.1–2.3）
# 本程式展示：字串分割、開頭/結尾檢查、Shell 通配符匹配的用法

# ================================================================================
# 【引入模組】
# ================================================================================
import re  # 引入正則表達式模組（用於複雜的字串分割）
from fnmatch import fnmatch, fnmatchcase  # 引入通配符匹配函數

# ================================================================================
# 【2.1 多界定符分割】使用 re.split() 用多種分隔符號分割字串
# ================================================================================

# 定義一個包含多種分隔符號的字串
# 分隔符號有：分號 (;)、逗號 (,)、空格 ( )
line = "asdf fjdk; afed, fjek,asdf, foo"

# 使用正則表達式分割：
# [;,\s] 表示「分號或逗號或空格」
# \s* 表示「0 個或多個額外的空格」（用來清除多餘空格）
# r"..." 是原始字串，避免反斜線被轉義
print("【方法 1】使用字符集 [;,\\s]：")
print(re.split(r"[;,\s]\s*", line))
# 輸出結果：['asdf', 'fjdk', 'afed', 'fjek', 'asdf', 'foo']

print()  # 空行，讓輸出更清楚

# 使用非捕獲分組方式分割（結果相同）：
# (?:,|;|\s) 表示「逗號或分號或空格」，但不「捕獲」這個符號
# （不捕獲就是不會在結果中保留分隔符號）
print("【方法 2】使用非捕獲分組 (?:,|;|\\s)：")
print(re.split(r"(?:,|;|\s)\s*", line))
# 輸出結果：['asdf', 'fjdk', 'afed', 'fjek', 'asdf', 'foo']

# ================================================================================
# 【2.2 開頭/結尾匹配】使用 startswith() 和 endswith() 方法
# ================================================================================

print()  # 空行

# 定義一個檔案名稱
filename = "spam.txt"

# 檢查字串是否以 ".txt" 結尾
# endswith() 方法會回傳 True（結尾相符）或 False（結尾不符）
print("【startswith / endswith 基礎用法】")
print(f"'{filename}' 是否以 '.txt' 結尾？{filename.endswith('.txt')}")  # 輸出：True
print(f"'{filename}' 是否以 'file:' 開頭？{filename.startswith('file:')}")  # 輸出：False

print()  # 空行

# 同時檢查多種後綴名
# 傳入 tuple（用括號 ），不能傳 list（用方括號 []）
filenames = ["Makefile", "foo.c", "bar.py", "spam.c", "spam.h"]

# 列表推導式：篩選所有以 ".c" 或 ".h" 結尾的檔案
# 如果 name.endswith((".c", ".h")) 為 True，就將 name 加入新列表
print("【檢查多種後綴】從以下檔案中找出 C 語言檔案：")
print(f"原始列表：{filenames}")
print("找到的 C 語言檔案：")
print([name for name in filenames if name.endswith((".c", ".h"))])
# 輸出結果：['foo.c', 'spam.c', 'spam.h']

# ================================================================================
# 【2.3 Shell 通配符匹配】使用 fnmatch() 進行模式匹配
# ================================================================================

print()  # 空行

# fnmatch() 使用 Unix Shell 通配符進行匹配
# * 表示「任意字元」
# [0-9] 表示「任何一個數字」

print("【fnmatch 基礎用法】")
# 檢查 "foo.txt" 是否符合模式 "*.txt"（任何以 .txt 結尾的檔案）
print(f"'foo.txt' 是否符合模式 '*.txt'？{fnmatch('foo.txt', '*.txt')}")  # 輸出：True

# 檢查 "Dat45.csv" 是否符合模式 "Dat[0-9]*"（以 Dat 開頭，後面跟著至少一個數字的檔案）
# 輸出：True
print(f"'Dat45.csv' 是否符合模式 'Dat[0-9]*'？{fnmatch('Dat45.csv', 'Dat[0-9]*')}")

print()  # 空行

# fnmatchcase() 強制區分大小寫（預設 fnmatch 不區分）
# "foo.txt" 與 "*.TXT" 比較時，因為大小寫不同，所以不符合
print("【fnmatchcase 區分大小寫】")
# 輸出：False
print(f"'foo.txt' 是否符合模式 '*.TXT'（區分大小寫）？{fnmatchcase('foo.txt', '*.TXT')}")

print()  # 空行

# 使用通配符篩選地址列表
addresses = ["5412 N CLARK ST", "1060 W ADDISON ST", "1039 W GRANVILLE AVE"]

# 篩選所有以 " ST"（空格+ST）結尾的地址
# fnmatchcase(a, "* ST") 表示「以任意字元開頭，以 ' ST' 結尾」
print("【實用例子】從地址列表中找出街名以 'ST' 結尾的地址：")
print(f"原始地址列表：{addresses}")
print("找到的 ST 街地址：")
print([a for a in addresses if fnmatchcase(a, "* ST")])
# 輸出結果：['5412 N CLARK ST', '1060 W ADDISON ST']
