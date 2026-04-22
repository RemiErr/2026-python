import sys
from collections import deque


def build_finish_order(graph):
    node_count = len(graph) - 1
    visited = [False] * (node_count + 1)
    order = []

    for start in range(1, node_count + 1):
        if visited[start]:
            continue

        stack = [(start, 0)]
        visited[start] = True

        while stack:
            node, edge_index = stack[-1]
            if edge_index < len(graph[node]):
                next_node = graph[node][edge_index]
                stack[-1] = (node, edge_index + 1)
                if not visited[next_node]:
                    visited[next_node] = True
                    stack.append((next_node, 0))
            else:
                order.append(node)
                stack.pop()

    return order


def build_scc(graph, reverse_graph, cash, is_bar):
    order = build_finish_order(graph)
    node_count = len(graph) - 1
    component_id = [-1] * (node_count + 1)
    component_cash = []
    component_bar = []
    current_component = 0

    for start in reversed(order):
        if component_id[start] != -1:
            continue

        total_cash = 0
        has_bar = False
        stack = [start]
        component_id[start] = current_component

        while stack:
            node = stack.pop()
            total_cash += cash[node]
            has_bar = has_bar or is_bar[node]

            for next_node in reverse_graph[node]:
                if component_id[next_node] == -1:
                    component_id[next_node] = current_component
                    stack.append(next_node)

        component_cash.append(total_cash)
        component_bar.append(has_bar)
        current_component += 1

    return component_id, component_cash, component_bar


def solve(text):
    data = list(map(int, text.split()))
    if not data:
        return ""

    index = 0
    node_count = data[index]
    edge_count = data[index + 1]
    index += 2

    graph = [[] for _ in range(node_count + 1)]
    reverse_graph = [[] for _ in range(node_count + 1)]

    for _ in range(edge_count):
        start = data[index]
        end = data[index + 1]
        index += 2
        graph[start].append(end)
        reverse_graph[end].append(start)

    cash = [0] * (node_count + 1)
    for node in range(1, node_count + 1):
        cash[node] = data[index]
        index += 1

    start_node = data[index]
    bar_count = data[index + 1]
    index += 2

    is_bar = [False] * (node_count + 1)
    for _ in range(bar_count):
        is_bar[data[index]] = True
        index += 1

    component_id, component_cash, component_bar = build_scc(graph, reverse_graph, cash, is_bar)
    component_count = len(component_cash)
    dag = [[] for _ in range(component_count)]
    indegree = [0] * component_count

    for node in range(1, node_count + 1):
        from_component = component_id[node]
        for next_node in graph[node]:
            to_component = component_id[next_node]
            if from_component != to_component:
                dag[from_component].append(to_component)
                indegree[to_component] += 1

    start_component = component_id[start_node]
    best = [-1] * component_count
    best[start_component] = component_cash[start_component]
    queue = deque(component for component in range(component_count) if indegree[component] == 0)

    while queue:
        component = queue.popleft()

        for next_component in dag[component]:
            if best[component] != -1:
                candidate = best[component] + component_cash[next_component]
                if candidate > best[next_component]:
                    best[next_component] = candidate

            indegree[next_component] -= 1
            if indegree[next_component] == 0:
                queue.append(next_component)

    answer = 0
    for component in range(component_count):
        if component_bar[component] and best[component] > answer:
            answer = best[component]

    return str(answer)


if __name__ == "__main__":
    sys.stdout.write(solve(sys.stdin.read()))
