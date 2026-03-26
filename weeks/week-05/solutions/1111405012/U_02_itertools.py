# Understand（理解）- itertools 工具函數
# 這份版本保留原始程式，並補上繁體中文註解，說明各工具適合的使用情境。

from itertools import islice, dropwhile, takewhile, chain, permutations, combinations

print("--- islice() 切片 ---")


def count(n):
    # 這是一個無窮生成器，會從 n 開始一直往上數。
    i = n
    while True:
        yield i
        i += 1


c = count(0)
# islice() 可以像切片一樣，只取出迭代器中的某一段資料。
result = list(islice(c, 5, 10))
print(f"islice(c, 5, 10): {result}")

print("\n--- dropwhile() 條件跳過 ---")
nums = [1, 3, 5, 2, 4, 6]

# dropwhile() 會在條件為 True 時持續略過元素，
# 一旦第一次遇到 False，後面元素就全部保留。
result = list(dropwhile(lambda x: x < 5, nums))
print(f"dropwhile(x<5, {nums}): {result}")

print("\n--- takewhile() 條件取用 ---")
# takewhile() 則相反：條件一旦第一次變成 False，就停止取值。
result = list(takewhile(lambda x: x < 5, nums))
print(f"takewhile(x<5, {nums}): {result}")

print("\n--- chain() 串聯 ---")
a = [1, 2]
b = [3, 4]
c = [5]

# chain() 會把多個可迭代物件視為一條連續資料流。
print(f"chain(a, b, c): {list(chain(a, b, c))}")

print("\n--- permutations() 排列 ---")
items = ["a", "b", "c"]
print(f"permutations(items):")

# permutations() 會考慮順序，因此 ('a', 'b') 與 ('b', 'a') 算不同結果。
for p in permutations(items):
    print(f"  {p}")

print(f"permutations(items, 2):")
for p in permutations(items, 2):
    print(f"  {p}")

print("\n--- combinations() 組合 ---")
print(f"combinations(items, 2):")

# combinations() 不考慮順序，所以 ('a', 'b') 和 ('b', 'a') 只算一種。
for c in combinations(items, 2):
    print(f"  {c}")

print("\n--- 組合應用：密碼窮舉 ---")
chars = ["A", "B", "1"]
print("2位數密碼:")

# 這裡用排列示範「字元不可重複且順序有差」的情境。
for p in permutations(chars, 2):
    print(f"  {''.join(p)}")

print("2位數密碼（可重複）:")
from itertools import combinations_with_replacement

# combinations_with_replacement() 允許元素重複出現，
# 但仍然屬於組合，所以順序不區分先後。
for p in combinations_with_replacement(chars, 2):
    print(f"  {''.join(p)}")
