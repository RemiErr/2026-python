import sys


def dedupe_preserve(nums):
    seen = set()
    result = []
    for num in nums:
        if num not in seen:  # 確保不重複
            seen.add(num)
            result.append(num)
    return result


def process_numbers(nums):
    # 輸出的資料結構
    return {
        "dedupe": dedupe_preserve(nums),
        "asc": sorted(nums),
        "desc": sorted(nums, reverse=True),
        "evens": [num for num in nums if num % 2 == 0],
    }


def format_line(prefix, items):
    if not items:
        return f"{prefix}:"
    return f"{prefix}: " + " ".join(str(item) for item in items)


def format_output(result):
    return [
        format_line("dedupe", result["dedupe"]),
        format_line("asc", result["asc"]),
        format_line("desc", result["desc"]),
        format_line("evens", result["evens"]),
    ]


def main():
    raw = sys.stdin.readline()  # 只抓一行資料
    nums = list(map(int, raw.split())) if raw else []
    result = process_numbers(nums)
    for line in format_output(result):
        print(line)


if __name__ == "__main__":
    main()
