"""依輸入的兩個整數，計算並輸出它們的絕對差值。"""

from __future__ import annotations


def solve(data: str) -> str:
    outputs: list[str] = []

    for line in data.splitlines():
        # 跳過空白行，避免 split 後資料不足。
        if not line.strip():
            continue
        parts = line.split()
        if len(parts) < 2:
            continue

        # 每行只取前兩個數字，輸出兩者差值的絕對值。
        a, b = int(parts[0]), int(parts[1])
        outputs.append(str(abs(a - b)))

    return "\n".join(outputs)


def main() -> None:
    import sys

    result = solve(sys.stdin.read())
    if result:
        sys.stdout.write(result + "\n")


if __name__ == "__main__":
    main()
