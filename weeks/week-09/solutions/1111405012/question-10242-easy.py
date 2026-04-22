import sys
from collections import deque


def make_order(graph):
    n = len(graph) - 1
    seen = [False] * (n + 1)
    order = []

    for start in range(1, n + 1):
        if seen[start]:
            continue

        stack = [(start, 0)]
        seen[start] = True

        while stack:
            node, idx = stack[-1]
            if idx < len(graph[node]):
                nxt = graph[node][idx]
                stack[-1] = (node, idx + 1)
                if not seen[nxt]:
                    seen[nxt] = True
                    stack.append((nxt, 0))
            else:
                order.append(node)
                stack.pop()

    return order


def make_scc(graph, rev, money, bars):
    order = make_order(graph)
    n = len(graph) - 1
    group = [-1] * (n + 1)
    group_money = []
    group_bar = []
    gid = 0

    for start in reversed(order):
        if group[start] != -1:
            continue

        total = 0
        has_bar = False
        stack = [start]
        group[start] = gid

        while stack:
            node = stack.pop()
            total += money[node]
            has_bar = has_bar or bars[node]

            for nxt in rev[node]:
                if group[nxt] == -1:
                    group[nxt] = gid
                    stack.append(nxt)

        group_money.append(total)
        group_bar.append(has_bar)
        gid += 1

    return group, group_money, group_bar


def solve(text):
    nums = list(map(int, text.split()))
    if not nums:
        return ""

    pos = 0
    n = nums[pos]
    m = nums[pos + 1]
    pos += 2

    graph = [[] for _ in range(n + 1)]
    rev = [[] for _ in range(n + 1)]

    for _ in range(m):
        a = nums[pos]
        b = nums[pos + 1]
        pos += 2
        graph[a].append(b)
        rev[b].append(a)

    money = [0] * (n + 1)
    for node in range(1, n + 1):
        money[node] = nums[pos]
        pos += 1

    start = nums[pos]
    p = nums[pos + 1]
    pos += 2

    bars = [False] * (n + 1)
    for _ in range(p):
        bars[nums[pos]] = True
        pos += 1

    group, group_money, group_bar = make_scc(graph, rev, money, bars)
    group_count = len(group_money)
    dag = [[] for _ in range(group_count)]
    indeg = [0] * group_count

    for node in range(1, n + 1):
        g1 = group[node]
        for nxt in graph[node]:
            g2 = group[nxt]
            if g1 != g2:
                dag[g1].append(g2)
                indeg[g2] += 1

    start_group = group[start]
    best = [-1] * group_count
    best[start_group] = group_money[start_group]
    q = deque(i for i in range(group_count) if indeg[i] == 0)

    # 壓縮後一定是 DAG，所以可以直接做拓樸 DP。
    while q:
        now = q.popleft()

        for nxt in dag[now]:
            if best[now] != -1:
                cand = best[now] + group_money[nxt]
                if cand > best[nxt]:
                    best[nxt] = cand

            indeg[nxt] -= 1
            if indeg[nxt] == 0:
                q.append(nxt)

    answer = 0
    for gid in range(group_count):
        if group_bar[gid] and best[gid] > answer:
            answer = best[gid]

    return str(answer)


if __name__ == "__main__":
    sys.stdout.write(solve(sys.stdin.read()))
