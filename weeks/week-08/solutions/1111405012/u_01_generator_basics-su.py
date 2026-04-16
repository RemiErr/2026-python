def frange(start, stop, step):
    current = start
    while current < stop:
        yield current
        current += step


def countdown(n):
    for number in range(n, 0, -1):
        yield number


def fibonacci():
    first = 0
    second = 1
    while True:
        yield first
        first, second = second, first + second


def first_n_fibonacci(count):
    fib = fibonacci()
    result = []
    for _ in range(count):
        result.append(next(fib))
    return result


def chain_iter(*iterables):
    for iterable in iterables:
        for item in iterable:
            yield item


class Node:
    def __init__(self, value):
        self.value = value
        self.children = []

    def add_child(self, node):
        self.children.append(node)

    def depth_first(self):
        yield self
        for child in self.children:
            yield from child.depth_first()


def build_sample_tree():
    root = Node(0)
    child_one = Node(1)
    child_two = Node(2)
    child_one.add_child(Node(3))
    child_one.add_child(Node(4))
    root.add_child(child_one)
    root.add_child(child_two)
    return root


def depth_first_values(root):
    result = []
    for node in root.depth_first():
        result.append(node.value)
    return result


def flatten(items):
    for item in items:
        if isinstance(item, list):
            for value in flatten(item):
                yield value
        else:
            yield item


def build_demo_lines():
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
