# Remember（記憶）- 迭代器基礎概念
# 這份版本保留原始程式，並補上繁體中文註解，方便對照每個範例在示範什麼。

# 1. 迭代器協議的核心方法
items = [1, 2, 3]

# iter() 會向可迭代物件索取「迭代器」。
# 對 list 來說，等同於呼叫它的 __iter__()。
it = iter(items)
print(f"迭代器: {it}")

# next() 會讓迭代器往前走一步，底層概念等同呼叫 __next__()。
print(f"第一個: {next(it)}")  # 1
print(f"第二個: {next(it)}")  # 2
print(f"第三個: {next(it)}")  # 3

# 沒有更多元素時，迭代器必須丟出 StopIteration，
# 這也是 for 迴圈判斷「資料取完」的依據。
try:
    next(it)
except StopIteration:
    print("迭代結束!")

# 2. 常見可迭代物件
print("\n--- 常見可迭代物件 ---")

# 列表
print(f"列表 iter: {iter([1, 2, 3])}")

# 字串
print(f"字串 iter: {iter('abc')}")

# 字典
# 直接對 dict 做 iter() 時，預設會走訪 key。
print(f"字典 iter: {iter({'a': 1, 'b': 2})}")

# 檔案
# 檔案物件也能逐行迭代，這裡用 StringIO 模擬檔案內容。
import io

f = io.StringIO("line1\nline2\nline3")
print(f"檔案 iter: {iter(f)}")


# 3. 自訂可迭代物件
class CountDown:
    def __init__(self, start):
        self.start = start

    def __iter__(self):
        # 每次開始迭代時，都回傳一個新的倒數迭代器。
        # 這樣同一個 CountDown 物件可以被重新迭代。
        return CountDownIterator(self.start)


class CountDownIterator:
    def __init__(self, start):
        self.current = start

    def __next__(self):
        # 倒數到 0 以前持續回傳值，之後用 StopIteration 結束。
        if self.current <= 0:
            raise StopIteration
        self.current -= 1
        return self.current + 1


print("\n--- 自訂迭代器 ---")
for i in CountDown(3):
    print(i, end=" ")  # 3 2 1

# 4. 迭代器 vs 可迭代物件
print("\n\n--- 迭代器 vs 可迭代物件 ---")

# 列表是可迭代物件，不是迭代器；
# 它知道如何產生迭代器，但自己不負責記錄走到哪裡。
my_list = [1, 2, 3]
print(f"列表: 可迭代物件 ✓, 迭代器 ✗")

# 列表經過 iter() 後，才會得到真正能逐步取值的迭代器物件。
my_iter = iter(my_list)
print(f"iter(列表): 可迭代物件 ✗, 迭代器 ✓")

# 一般來說，完整的迭代器會同時具備 __iter__ 與 __next__；
# 這裡是概念示範，因此重點放在「可逐步取值」這件事。
print(f"迭代器: 可迭代物件 ✓ (有__iter__), 迭代器 ✓ (有__next__)")

# 5. StopIteration 例外
print("\n--- StopIteration 用法 ---")


# 手動遍歷（章節 4.1 風格）
def manual_iter(items):
    # 這段程式把 for 迴圈平常幫我們做的事手動寫出來。
    it = iter(items)
    while True:
        try:
            item = next(it)
            print(f"取得: {item}")
        except StopIteration:
            break


manual_iter(["a", "b", "c"])


# 使用預設值的版本
def manual_iter_default(items):
    # next(iterator, 預設值) 可以避免例外，改用判斷值來結束。
    # 這個示範假設資料本身不會出現 None。
    it = iter(items)
    while True:
        item = next(it, None)  # 預設值
        if item is None:
            break
        print(f"取得: {item}")


print("\n使用預設值:")
manual_iter_default(["a", "b", "c"])
