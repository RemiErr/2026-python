import sys
from collections import deque


sys.setrecursionlimit(1_000_000)


def read_input(text):
    numbers = list(map(int, text.split()))
    if not numbers:
        return None

    index = 0
    node_count = numbers[index]
    edge_count = numbers[index + 1]
    index += 2

    graph = [[] for _ in range(node_count + 1)]
    for _ in range(edge_count):
        start = numbers[index]
        end = numbers[index + 1]
        index += 2
        graph[start].append(end)

    money = [0] * (node_count + 1)
    for node in range(1, node_count + 1):
        money[node] = numbers[index]
        index += 1

    start_node = numbers[index]
    bar_count = numbers[index + 1]
    index += 2

    has_bar = [False] * (node_count + 1)
    for _ in range(bar_count):
        has_bar[numbers[index]] = True
        index += 1

    return graph, money, start_node, has_bar


def build_scc(graph, money, has_bar):
    """使用 Tarjan 演算法一次找出所有強連通分量。"""
    node_count = len(graph) - 1
    order = 0
    stack = []
    in_stack = [False] * (node_count + 1)
    discover = [-1] * (node_count + 1)
    low = [0] * (node_count + 1)
    component_id = [-1] * (node_count + 1)
    component_money = []
    component_bar = []

    def dfs(node):
        nonlocal order
        discover[node] = order
        low[node] = order
        order += 1
        stack.append(node)
        in_stack[node] = True

        for nxt in graph[node]:
            if discover[nxt] == -1:
                dfs(nxt)
                low[node] = min(low[node], low[nxt])
            elif in_stack[nxt]:
                low[node] = min(low[node], discover[nxt])

        if low[node] != discover[node]:
            return

        total_money = 0
        reach_bar = False
        cid = len(component_money)

        while True:
            current = stack.pop()
            in_stack[current] = False
            component_id[current] = cid
            total_money += money[current]
            reach_bar = reach_bar or has_bar[current]
            if current == node:
                break

        component_money.append(total_money)
        component_bar.append(reach_bar)

    for node in range(1, node_count + 1):
        if discover[node] == -1:
            dfs(node)

    return component_id, component_money, component_bar


def build_dag(graph, component_id, component_count):
    dag = [set() for _ in range(component_count)]
    indegree = [0] * component_count

    for node in range(1, len(graph)):
        from_id = component_id[node]
        for nxt in graph[node]:
            to_id = component_id[nxt]
            if from_id == to_id or to_id in dag[from_id]:
                continue
            dag[from_id].add(to_id)
            indegree[to_id] += 1

    return dag, indegree


def max_money_to_bar(graph, money, start_node, has_bar):
    component_id, component_money, component_bar = build_scc(graph, money, has_bar)
    component_count = len(component_money)
    dag, indegree = build_dag(graph, component_id, component_count)

    start_component = component_id[start_node]
    best = [-1] * component_count
    best[start_component] = component_money[start_component]
    queue = deque(
        cid for cid in range(component_count) if indegree[cid] == 0
    )

    while queue:
        cid = queue.popleft()

        for nxt in dag[cid]:
            if best[cid] != -1:
                candidate = best[cid] + component_money[nxt]
                if candidate > best[nxt]:
                    best[nxt] = candidate

            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)

    answer = 0
    for cid in range(component_count):
        if component_bar[cid] and best[cid] > answer:
            answer = best[cid]

    return str(answer)


def solve(text):
    parsed = read_input(text)
    if parsed is None:
        return ""
    return max_money_to_bar(*parsed)


if __name__ == "__main__":
    sys.stdout.write(solve(sys.stdin.read()))
