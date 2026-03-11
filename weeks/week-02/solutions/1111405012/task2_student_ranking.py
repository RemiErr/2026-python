import sys


def sort_students(students):
    # 回傳排序後的 List，排序方式使用 score 降序、age 升序、name 升序
    return sorted(students, key=lambda item: (-item[1], item[2], item[0]))


def top_k(students, k):
    # 抓出前 k 名學生
    if k <= 0:
        return []
    return sort_students(students)[:k]


def main():
    # 手動多行輸入可以用 Ctrl+Z 再 Enter
    lines = sys.stdin.read().strip().splitlines()
    if not lines:
        return

    n, k = map(int, lines[0].split())
    students = []
    for line in lines[1:1 + n]:
        name, score, age = line.split()
        students.append((name, int(score), int(age)))

    for name, score, age in top_k(students, k):
        print(f"{name} {score} {age}")


if __name__ == "__main__":
    main()
