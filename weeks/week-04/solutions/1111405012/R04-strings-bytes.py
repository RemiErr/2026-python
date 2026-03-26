# R04. 位元組字串操作（2.20）
# 繁體中文註解版：說明 bytes 和一般 str 的關鍵差異。
# bytes / bytearray 支援大部分字串方法，但有幾個重要差異

import re

data = b"Hello World"

# bytes 切片後，仍然得到 bytes。
print(data[0:5])  # b'Hello'
print(data.startswith(b"Hello"))  # True
print(data.split())  # [b'Hello', b'World']
print(data.replace(b"Hello", b"Hello Cruel"))  # b'Hello Cruel World'

# 正則表達式也必須使用 bytes 模式。
# 注意這裡是 rb"..."，不是一般字串 r"..."
raw = b"FOO:BAR,SPAM"
print(re.split(rb"[:,]", raw))  # [b'FOO', b'BAR', b'SPAM']

# 差異 1：str 索引回傳字元，bytes 索引回傳整數。
a = "Hello"
b = b"Hello"
print(a[0])  # 'H'（字元）
print(b[0])  # 72（整數，即 ord('H')）

# 差異 2：bytes 不能直接 format。
# 正確流程通常是：先組出字串，再 encode 成 bytes。
formatted = "{:10s} {:10d}".format("ACME", 100).encode("ascii")
print(formatted)  # b'ACME            100'
