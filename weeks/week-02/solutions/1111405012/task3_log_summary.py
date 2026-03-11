import sys
from collections import Counter


def summarize_logs(entries):
    # 統計所有使用者與動作的出現次數
    user_counts = Counter()
    action_counts = Counter()
    for user, action in entries:
        user_counts[user] += 1
        action_counts[action] += 1

    # 先依總數遞減，再依使用者名稱遞增排序
    users_sorted = sorted(user_counts.items(),
                          key=lambda item: (-item[1], item[0]))

    if not action_counts:
        return users_sorted, (None, 0)

    # 同次數時用字母順序決定 top action
    max_count = max(action_counts.values())
    top_actions = [action for action,
                   count in action_counts.items() if count == max_count]
    top_action = min(top_actions)
    return users_sorted, (top_action, max_count)


def main():
    lines = sys.stdin.read().strip().splitlines()
    if not lines:
        return

    first = lines[0].strip()
    m = int(first) if first else 0
    entries = []
    for line in lines[1:1 + m]:
        parts = line.split()
        if len(parts) >= 2:
            entries.append((parts[0], parts[1]))

    users_sorted, (top_action, top_count) = summarize_logs(entries)
    for user, count in users_sorted:
        print(f"{user} {count}")

    if top_action is None:
        print("top_action: None 0")
    else:
        print(f"top_action: {top_action} {top_count}")


if __name__ == "__main__":
    main()
