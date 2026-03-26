# U01. 字串分割與匹配的陷阱（2.1–2.11）
# 繁體中文註解版：專門補充新手最容易踩到的坑。
# 捕獲分組保留分隔符 / startswith 必須傳 tuple / strip 只處理頭尾

import re

# ── 捕獲分組保留分隔符（2.1）─────────────────────────
line = "asdf fjdk; afed, fjek,asdf, foo"

# 這裡用的是「捕獲分組」(...)，所以分隔符也會保留下來。
fields = re.split(r"(;|,|\s)\s*", line)

# 切開後的偶數索引是資料、奇數索引是分隔符。
values = fields[::2]  # 偶數索引 = 實際值
delimiters = fields[1::2] + [""]

# 重新把值和分隔符交錯接回去。
rebuilt = "".join(v + d for v, d in zip(values, delimiters))
print(rebuilt)  # 'asdf fjdk;afed,fjek,asdf,foo'

# ── startswith 必須傳 tuple（2.2）────────────────────
url = "http://www.python.org"
choices = ["http:", "ftp:"]

try:
    # startswith() / endswith() 接受字串或 tuple，不接受 list。
    url.startswith(choices)  # type: ignore[arg-type]
except TypeError as e:
    print(f"TypeError: {e}")  # 不能傳 list！

print(url.startswith(tuple(choices)))  # True（轉成 tuple 才行）

# ── strip 只處理頭尾，不處理中間（2.11）──────────────
s = "  hello     world  "

# strip() 只能清除字串前後的空白，不會碰中間的連續空格。
print(repr(s.strip()))  # 'hello     world'（中間多餘空白還在）

# replace(" ", "") 會把所有空格都砍掉，往往太激烈。
print(repr(s.replace(" ", "")))  # 'helloworld'（過頭，連詞間空白也消）

# 若只是想把「多個空白壓成一個」，可用正則表達式。
print(repr(re.sub(r"\s+", " ", s.strip())))  # 'hello world'（正確）

# 生成器逐行清理（高效，不預載入記憶體）
lines = ["  apple  \n", "  banana  \n"]
for line in (l.strip() for l in lines):
    print(line)
