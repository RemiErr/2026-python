"""UVA 948 簡單版：用兩張布林表記錄每枚硬幣是否可能偏重或偏輕。"""

from __future__ import annotations


def solve(data: str) -> str:
    # 題目中的空白行只是分隔資料，對判斷沒有影響，
    # 所以先全部拿掉，後面讀取會簡單很多。
    lines: list[str] = []
    for line in data.splitlines():
        line = line.strip()
        if line:
            lines.append(line)

    if not lines:
        return ""

    index = 0
    case_count = int(lines[index])
    index += 1

    answers: list[str] = []

    for _ in range(case_count):
        # 讀入這一組測試資料的硬幣數量 n 和秤重次數 k。
        n, k = map(int, lines[index].split())
        index += 1

        # heavy[i] = True 代表第 i 枚硬幣「還有可能偏重」。
        # light[i] = True 代表第 i 枚硬幣「還有可能偏輕」。
        # 一開始先假設每一枚硬幣兩種狀態都可能。
        heavy = [True] * (n + 1)
        light = [True] * (n + 1)

        for _ in range(k):
            numbers = list(map(int, lines[index].split()))
            index += 1

            result = lines[index]
            index += 1

            p = numbers[0]
            left = numbers[1 : 1 + p]
            right = numbers[1 + p : 1 + 2 * p]

            # 這一輪秤重結束後，只有符合結果的可能性可以留下來，
            # 所以先開兩張新的表來存「這次秤重之後仍然成立」的狀態。
            next_heavy = [False] * (n + 1)
            next_light = [False] * (n + 1)

            if result == "=":
                # 平衡代表天平上的硬幣都是真的，
                # 所以只有「沒上天平的硬幣」才可能繼續留下。
                left_set = set(left)
                right_set = set(right)

                for coin in range(1, n + 1):
                    if coin not in left_set and coin not in right_set:
                        next_heavy[coin] = heavy[coin]
                        next_light[coin] = light[coin]

            elif result == "<":
                # 左邊比較輕：
                # 1. 左盤上的假幣只能是「偏輕」
                # 2. 右盤上的假幣只能是「偏重」
                for coin in left:
                    if light[coin]:
                        next_light[coin] = True

                for coin in right:
                    if heavy[coin]:
                        next_heavy[coin] = True

            else:
                # 左邊比較重：
                # 1. 左盤上的假幣只能是「偏重」
                # 2. 右盤上的假幣只能是「偏輕」
                for coin in left:
                    if heavy[coin]:
                        next_heavy[coin] = True

                for coin in right:
                    if light[coin]:
                        next_light[coin] = True

            # 更新成最新的可能性，準備處理下一次秤重。
            heavy = next_heavy
            light = next_light

        # 題目只要求找出「哪一枚」是假幣，
        # 所以只要統計還剩下哪些硬幣可能是假幣即可。
        suspect_coins: list[int] = []
        for coin in range(1, n + 1):
            if heavy[coin] or light[coin]:
                suspect_coins.append(coin)

        if len(suspect_coins) == 1:
            answers.append(str(suspect_coins[0]))
        else:
            answers.append("0")

    # 題目要求不同測試資料之間要空一行。
    return "\n\n".join(answers)


def main() -> None:
    import sys

    result = solve(sys.stdin.read())
    if result:
        sys.stdout.write(result + "\n")


if __name__ == "__main__":
    main()
