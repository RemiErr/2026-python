"""用繁體中文整理生成器的核心概念。"""


def frange(start, stop, step):
    # 生成器可以一次只產生一個值，不需要先建立整串列表。
    current = start
    while current < stop:
        yield current
        current += step


def countdown(n):
    # 倒數生成器會從 n 一路產生到 1。
    while n > 0:
        yield n
        n -= 1


def fibonacci():
    # 這是一個無限生成器，會一直往後產生費波那契數列。
    a_value, b_value = 0, 1
    while True:
        yield a_value
        a_value, b_value = b_value, a_value + b_value


def first_n_fibonacci(count):
    # 只取前面幾個值，避免無限生成器停不下來。
    fib = fibonacci()
    result = []
    for _ in range(count):
        result.append(next(fib))
    return result


def chain_iter(*iterables):
    # yield from 可以把子序列的值直接接過來。
    for iterable in iterables:
        yield from iterable


class Node:
    # 簡單的樹節點，每個節點都可以有多個子節點。
    def __init__(self, value):
        self.value = value
        self.children = []

    def add_child(self, node):
        self.children.append(node)

    def __iter__(self):
        return iter(self.children)

    def depth_first(self):
        # 先走自己，再走所有子節點。
        yield self
        for child in self:
            yield from child.depth_first()


def build_sample_tree():
    # 建立和原始教材相同的小樹。
    root = Node(0)
    root.add_child(Node(1))
    root.add_child(Node(2))
    root.children[0].add_child(Node(3))
    root.children[0].add_child(Node(4))
    return root


def depth_first_values(root):
    return [node.value for node in root.depth_first()]


def flatten(items):
    # 巢狀列表遇到子列表時，再繼續往裡面展開。
    for item in items:
        if isinstance(item, list):
            yield from flatten(item)
        else:
            yield item


def build_demo_lines():
    # 固定整理成可閱讀、可測試的輸出內容。
    countdown_gen = countdown(3)

    return [
        "生成器概念",
        f"frange(0, 2, 0.5): {list(frange(0, 2, 0.5))}",
        "Starting countdown from 3",
        f"next(c): {next(countdown_gen)}",
        f"next(c): {next(countdown_gen)}",
        f"next(c): {next(countdown_gen)}",
        "Done!",
        "StopIteration!",
        f"Fibonacci 前 10 個: {first_n_fibonacci(10)}",
        f"chain_iter: {list(chain_iter([1, 2], [3, 4], [5, 6]))}",
        f"深度優先: {depth_first_values(build_sample_tree())}",
        f"展開: {list(flatten([1, [2, [3, 4]], 5]))}",
    ]


def render_demo():
    return "\n".join(build_demo_lines())


if __name__ == "__main__":
    print(render_demo())
