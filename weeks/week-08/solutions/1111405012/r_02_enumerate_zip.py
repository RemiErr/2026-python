"""用繁體中文整理 enumerate() 和 zip() 的基礎用法。"""

from itertools import zip_longest


def enumerate_colors(colors, start=0):
    # enumerate() 會把索引和值打包在一起。
    return list(enumerate(colors, start))


def number_lines(lines, start=1):
    # 常見做法是從 1 開始編行號。
    return list(enumerate(lines, start))


def pair_names_scores(names, scores):
    # zip() 會把兩個序列同位置的資料配成一組。
    return list(zip(names, scores))


def sum_three_lists(a_values, b_values, c_values):
    # 三個序列也可以一起 zip()。
    return [x + y + z for x, y, z in zip(a_values, b_values, c_values)]


def zip_shortest(left, right):
    # 一般 zip() 只會配到最短序列結束為止。
    return list(zip(left, right))


def zip_with_fill(left, right, fillvalue=0):
    # zip_longest() 可以保留較長的那一邊。
    return list(zip_longest(left, right, fillvalue=fillvalue))


def make_dict(keys, values):
    # dict(zip()) 是建立字典的常見招式。
    return dict(zip(keys, values))


def build_demo_lines():
    colors = ["red", "green", "blue"]
    names = ["Alice", "Bob", "Carol"]
    scores = [90, 85, 92]
    a_values = [1, 2, 3]
    b_values = [10, 20, 30]
    c_values = [100, 200, 300]
    x_values = [1, 2]
    y_values = ["a", "b", "c"]
    keys = ["name", "age", "city"]
    values = ["John", "30", "NYC"]

    return [
        "enumerate() 和 zip() 範例",
        f"enumerate(colors): {enumerate_colors(colors)}",
        f"enumerate(colors, 1): {enumerate_colors(colors, 1)}",
        f"行號: {number_lines(['line1', 'line2', 'line3'])}",
        f"配對姓名分數: {pair_names_scores(names, scores)}",
        f"三個串列相加: {sum_three_lists(a_values, b_values, c_values)}",
        f"zip 最短配對: {zip_shortest(x_values, y_values)}",
        f"zip_longest 配對: {zip_with_fill(x_values, y_values)}",
        f"建立字典: {make_dict(keys, values)}",
    ]


def render_demo():
    return "\n".join(build_demo_lines())


if __name__ == "__main__":
    print(render_demo())
