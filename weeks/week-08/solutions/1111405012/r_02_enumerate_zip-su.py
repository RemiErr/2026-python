from itertools import zip_longest


def enumerate_colors(colors, start=0):
    return list(enumerate(colors, start))


def number_lines(lines, start=1):
    return list(enumerate(lines, start))


def pair_names_scores(names, scores):
    return list(zip(names, scores))


def sum_three_lists(a_values, b_values, c_values):
    result = []
    for x, y, z in zip(a_values, b_values, c_values):
        result.append(x + y + z)
    return result


def zip_shortest(left, right):
    return list(zip(left, right))


def zip_with_fill(left, right, fillvalue=0):
    return list(zip_longest(left, right, fillvalue=fillvalue))


def make_dict(keys, values):
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
