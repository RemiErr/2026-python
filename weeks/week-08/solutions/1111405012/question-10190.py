import math
from sys import stdin, stdout


EPSILON = 1e-10


def clamp(value, low, high):
    return max(low, min(high, value))


def normalize_velocity(position, max_left, velocity):
    """如果剛好在邊界又朝外走，立刻把方向反過來。"""
    if abs(position) <= EPSILON and velocity < 0:
        return -velocity
    if abs(position - max_left) <= EPSILON and velocity > 0:
        return -velocity
    return velocity


def time_to_wall(position, max_left, velocity):
    """算出多久後會碰到左右邊界。"""
    if velocity > 0:
        return (max_left - position) / velocity
    if velocity < 0:
        return position / (-velocity)
    return math.inf


def covered_length_at(states, moment):
    """計算某一個時間點被雨傘遮住的總長度。"""
    intervals = []

    for state in states:
        left = state["left"] + state["velocity"] * moment
        left = clamp(left, 0.0, state["max_left"])
        right = left + state["length"]
        intervals.append((left, right))

    intervals.sort()

    covered = 0.0
    current_left = None
    current_right = None

    for left, right in intervals:
        if current_left is None:
            current_left = left
            current_right = right
            continue

        if left > current_right:
            covered += current_right - current_left
            current_left = left
            current_right = right
        else:
            current_right = max(current_right, right)

    if current_left is not None:
        covered += current_right - current_left

    return covered


def integrate_segment(states, duration):
    """在速度固定的一小段時間內，精確積分遮蔽長度。"""
    if duration <= EPSILON:
        return 0.0

    endpoints = []
    for state in states:
        left = state["left"]
        right = left + state["length"]
        velocity = state["velocity"]
        endpoints.append((left, velocity))
        endpoints.append((right, velocity))

    moments = [0.0, duration]

    for index in range(len(endpoints)):
        start_a, speed_a = endpoints[index]
        for other in range(index + 1, len(endpoints)):
            start_b, speed_b = endpoints[other]
            if abs(speed_a - speed_b) <= EPSILON:
                continue

            meet_time = (start_b - start_a) / (speed_a - speed_b)
            if EPSILON < meet_time < duration - EPSILON:
                moments.append(meet_time)

    moments.sort()

    unique_moments = []
    for moment in moments:
        if not unique_moments or abs(moment - unique_moments[-1]) > EPSILON:
            unique_moments.append(moment)

    total = 0.0
    for index in range(len(unique_moments) - 1):
        start = unique_moments[index]
        end = unique_moments[index + 1]
        covered_start = covered_length_at(states, start)
        covered_end = covered_length_at(states, end)
        total += (covered_start + covered_end) * (end - start) / 2.0

    return total


def solve_case(count, width, total_time, rain_volume, umbrellas):
    """模擬所有雨傘的往返運動，累計落到路面的雨量。"""
    states = []
    for left, length, velocity in umbrellas:
        max_left = width - length
        states.append(
            {
                "left": float(left),
                "length": float(length),
                "velocity": float(velocity),
                "max_left": float(max_left),
            }
        )

    current_time = 0.0
    answer = 0.0

    while current_time + EPSILON < total_time:
        remaining = total_time - current_time

        for state in states:
            state["velocity"] = normalize_velocity(
                state["left"], state["max_left"], state["velocity"]
            )

        next_hit = remaining
        for state in states:
            hit_time = time_to_wall(state["left"], state["max_left"], state["velocity"])
            if hit_time < next_hit:
                next_hit = hit_time

        duration = min(remaining, next_hit)
        covered_area = integrate_segment(states, duration)
        answer += (width * duration - covered_area) * rain_volume

        for state in states:
            state["left"] += state["velocity"] * duration
            state["left"] = clamp(state["left"], 0.0, state["max_left"])

        current_time += duration

        for state in states:
            hit_time = time_to_wall(state["left"], state["max_left"], state["velocity"])
            if abs(hit_time) <= EPSILON:
                state["velocity"] = -state["velocity"]

        if duration <= EPSILON:
            break

    return f"{answer:.2f}"


def solve(text):
    """依照題目內文，處理單一組自動傘資料。"""
    tokens = text.split()
    if len(tokens) < 4:
        return ""

    count = int(tokens[0])
    width = float(tokens[1])
    total_time = float(tokens[2])
    rain_volume = float(tokens[3])

    umbrellas = []
    index = 4
    for _ in range(count):
        left = float(tokens[index])
        length = float(tokens[index + 1])
        velocity = float(tokens[index + 2])
        umbrellas.append((left, length, velocity))
        index += 3

    return solve_case(count, width, total_time, rain_volume, umbrellas)


def main():
    result = solve(stdin.read())
    if result:
        stdout.write(result)


if __name__ == "__main__":
    main()
