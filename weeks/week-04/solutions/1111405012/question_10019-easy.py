"""UVA 10019 簡單版：每行讀兩個整數，輸出它們的絕對差。"""

from __future__ import annotations


def solve(data: str) -> str:
    answers: list[str] = []

    for line in data.splitlines():
        # 空白行沒有資料，直接跳過。
        line = line.strip()
        if not line:
            continue

        parts = line.split()
        if len(parts) < 2:
            continue

        # 題目每行只要兩個整數。
        # 不用管誰比較大，直接用 abs 取絕對值最簡單。
        a = int(parts[0])
        b = int(parts[1])
        answers.append(str(abs(a - b)))

    return "\n".join(answers)


def main() -> None:
    import sys

    result = solve(sys.stdin.read())
    if result:
        sys.stdout.write(result + "\n")


if __name__ == "__main__":
    main()
