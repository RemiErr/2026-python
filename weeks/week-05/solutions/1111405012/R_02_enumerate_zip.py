# Remember（記憶）- enumerate() 和 zip()
# 這份版本保留原始範例，並補上繁體中文註解，說明兩個常用迭代工具的用途。

colors = ["red", "green", "blue"]

print("--- enumerate() 基本用法 ---")
# enumerate() 會在走訪元素時，同時提供索引與值。
for i, color in enumerate(colors):
    print(f"{i}: {color}")

print("\n--- enumerate(start=1) ---")
# start=1 可把索引起點改成 1，常用在顯示「第幾筆資料」。
for i, color in enumerate(colors, 1):
    print(f"第{i}個: {color}")

print("\n--- enumerate with 檔案 ---")
# 雖然這裡用的是 list，實務上 enumerate 很常搭配檔案逐行處理。
lines = ["line1", "line2", "line3"]
for lineno, line in enumerate(lines, 1):
    print(f"行 {lineno}: {line}")

print("\n--- zip() 基本用法 ---")
names = ["Alice", "Bob", "Carol"]
scores = [90, 85, 92]

# zip() 會把多個序列依照相同位置配對在一起。
for name, score in zip(names, scores):
    print(f"{name}: {score}")

print("\n--- zip() 多個序列 ---")
a = [1, 2, 3]
b = [10, 20, 30]
c = [100, 200, 300]

# zip() 不只可以配對兩個序列，也能同時合併三個以上。
for x, y, z in zip(a, b, c):
    print(f"{x} + {y} + {z} = {x + y + z}")

print("\n--- zip() 長度不同 ---")
x = [1, 2]
y = ["a", "b", "c"]

# 一般 zip() 會以最短序列為準，多出來的元素會被忽略。
print(f"list(zip(x, y)): {list(zip(x, y))}")

from itertools import zip_longest

# zip_longest() 會保留較長序列的剩餘元素，
# 缺的部分用 fillvalue 補上。
print(f"zip_longest: {list(zip_longest(x, y, fillvalue=0))}")

print("\n--- 建立字典 ---")
keys = ["name", "age", "city"]
values = ["John", "30", "NYC"]

# dict(zip(...)) 是把 keys 與 values 組成字典的典型寫法。
d = dict(zip(keys, values))
print(f"dict: {d}")
