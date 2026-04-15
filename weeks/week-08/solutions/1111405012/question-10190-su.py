import math
from sys import stdin, stdout


EPS = 1e-10


def union_length(states, t):
    parts = []
    for left, length, speed, limit in states:
        now_left = left + speed * t
        if now_left < 0:
            now_left = 0.0
        if now_left > limit:
            now_left = limit
        parts.append((now_left, now_left + length))

    parts.sort()

    total = 0.0
    if not parts:
        return total

    cur_l, cur_r = parts[0]
    for left, right in parts[1:]:
        if left > cur_r:
            total += cur_r - cur_l
            cur_l, cur_r = left, right
        else:
            cur_r = max(cur_r, right)

    total += cur_r - cur_l
    return total


def segment_area(states, dt):
    if dt <= EPS:
        return 0.0

    points = [0.0, dt]
    endpoints = []

    for left, length, speed, _ in states:
        endpoints.append((left, speed))
        endpoints.append((left + length, speed))

    for i in range(len(endpoints)):
        p1, v1 = endpoints[i]
        for j in range(i + 1, len(endpoints)):
            p2, v2 = endpoints[j]
            if abs(v1 - v2) <= EPS:
                continue

            t = (p2 - p1) / (v1 - v2)
            if EPS < t < dt - EPS:
                points.append(t)

    points.sort()

    clean_points = []
    for point in points:
        if not clean_points or abs(point - clean_points[-1]) > EPS:
            clean_points.append(point)

    area = 0.0
    for i in range(len(clean_points) - 1):
        t1 = clean_points[i]
        t2 = clean_points[i + 1]
        l1 = union_length(states, t1)
        l2 = union_length(states, t2)
        area += (l1 + l2) * (t2 - t1) / 2.0

    return area


def main():
    data = stdin.read().split()
    if len(data) < 4:
        return

    n = int(data[0])
    w = float(data[1])
    total_time = float(data[2])
    v = float(data[3])

    states = []
    index = 4
    for _ in range(n):
        x = float(data[index])
        length = float(data[index + 1])
        speed = float(data[index + 2])
        index += 3

        limit = w - length

        if abs(x) <= EPS and speed < 0:
            speed = -speed
        if abs(x - limit) <= EPS and speed > 0:
            speed = -speed

        states.append([x, length, speed, limit])

    now = 0.0
    answer = 0.0

    while now + EPS < total_time:
        rest = total_time - now
        dt = rest

        for state in states:
            x, length, speed, limit = state
            if speed > 0:
                dt = min(dt, (limit - x) / speed)
            elif speed < 0:
                dt = min(dt, x / (-speed))

        covered_area = segment_area(states, dt)
        answer += (w * dt - covered_area) * v

        for state in states:
            state[0] += state[2] * dt
            if state[0] < 0:
                state[0] = 0.0
            if state[0] > state[3]:
                state[0] = state[3]

        now += dt

        for state in states:
            if abs(state[0]) <= EPS and state[2] < 0:
                state[2] = -state[2]
            elif abs(state[0] - state[3]) <= EPS and state[2] > 0:
                state[2] = -state[2]

        if dt <= EPS:
            break

    stdout.write(f"{answer:.2f}")


if __name__ == "__main__":
    main()
