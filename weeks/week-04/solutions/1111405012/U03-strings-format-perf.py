# U03. 字串格式化效能與陷阱（2.14–2.20）
# 繁體中文註解版：把效能與錯誤用法放在同一支範例中。
# join vs + / format_map 缺失鍵 / bytes 索引差異

import timeit

# ── join 效能優於 + （2.14）──────────────────────────
parts = [f"item{i}" for i in range(1000)]


def bad_concat():
    s = ""
    for p in parts:
        # 每次 += 都會建立新的字串，資料量大時成本高。
        s += p  # 每次建立新字串，O(n²)
    return s


def good_join():
    # 先收集好片段，再一次合併，通常效率更好。
    return "".join(parts)  # 一次分配，O(n)


t1 = timeit.timeit(bad_concat, number=500)
t2 = timeit.timeit(good_join, number=500)
print(f"+串接: {t1:.3f}s  join: {t2:.3f}s")


# ── format_map 處理缺失鍵（2.15）─────────────────────
class SafeSub(dict):
    def __missing__(self, key: str) -> str:
        # 若 key 不存在，就把原佔位符保留回去，而不是直接丟 KeyError。
        return "{" + key + "}"  # 缺失時保留佔位符


name = "Guido"
s = "{name} has {n} messages."
print(s.format_map(SafeSub(vars())))  # 'Guido has {n} messages.'（n 不存在也不報錯）

# ── bytes 索引回傳整數（2.20）────────────────────────
a = "Hello"
b = b"Hello"
print(a[0])  # 'H'（字元）
print(b[0])  # 72（整數 = ord('H')）

# bytes 不能直接 format，需先格式化再 encode
print("{:10s} {:5d}".format("ACME", 100).encode("ascii"))
# b'ACME            100'
