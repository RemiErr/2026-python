# Understand（理解）- 生成器概念
# 這份版本保留原始程式，並補上繁體中文註解，聚焦說明 yield 與 yield from 的行為。


def frange(start, stop, step):
    # frange 模擬「浮點數版的 range」。
    # 每次執行到 yield 時會暫停，下一次 next() 再從原位置繼續。
    x = start
    while x < stop:
        yield x
        x += step


result = list(frange(0, 2, 0.5))
print(f"frange(0, 2, 0.5): {result}")


def countdown(n):
    # 生成器函式在真正被迭代前，不會先把所有值都算出來。
    print(f"Starting countdown from {n}")
    while n > 0:
        yield n
        n -= 1
    print("Done!")


print("\n--- 建立生成器 ---")
c = countdown(3)
print(f"生成器物件: {c}")

print("\n--- 逐步迭代 ---")
# 每呼叫一次 next(c)，countdown 就往下執行到下一個 yield。
print(f"next(c): {next(c)}")
print(f"next(c): {next(c)}")
print(f"next(c): {next(c)}")

try:
    next(c)
except StopIteration:
    print("StopIteration!")


def fibonacci():
    # 無窮生成器：理論上可以一直產生下一個值，
    # 因此通常會搭配 for、islice 或手動控制取用次數。
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


print("\n--- Fibonacci 生成器 ---")
fib = fibonacci()
for i in range(10):
    print(next(fib), end=" ")
print()


def chain_iter(*iterables):
    # yield from 會把子可迭代物件中的值逐一轉交出去，
    # 可以少寫一層 for 迴圈。
    for it in iterables:
        yield from it


print("\n--- yield from 用法 ---")
result = list(chain_iter([1, 2], [3, 4], [5, 6]))
print(f"chain_iter: {result}")


class Node:
    def __init__(self, value):
        self.value = value
        self.children = []

    def add_child(self, node):
        self.children.append(node)

    def __iter__(self):
        # 讓 Node 物件本身可直接被 for 迴圈走訪其子節點。
        return iter(self.children)

    def depth_first(self):
        # 深度優先走訪：
        # 先回傳自己，再遞迴走訪每個子節點。
        yield self
        for child in self:
            yield from child.depth_first()


print("\n--- 樹的深度優先遍歷 ---")
root = Node(0)
root.add_child(Node(1))
root.add_child(Node(2))
root.children[0].add_child(Node(3))
root.children[0].add_child(Node(4))

for node in root.depth_first():
    print(node.value, end=" ")
print()


def flatten(items):
    # 把巢狀結構遞迴攤平。
    # 這裡排除 str，是因為字串本身可迭代，若不排除會被拆成單一字元。
    for x in items:
        if hasattr(x, "__iter__") and not isinstance(x, str):
            yield from flatten(x)
        else:
            yield x


print("\n--- 巢狀序列攤平 ---")
nested = [1, [2, [3, 4]], 5]
print(f"展開: {list(flatten(nested))}")
