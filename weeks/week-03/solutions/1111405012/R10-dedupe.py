# R10. 去重且保序（1.10）

# 1. 基本版：去重且保留原順序（用 generator）
def dedupe(items):
    seen = set()
    for item in items:
        if item not in seen:
            yield item
            seen.add(item)


# 2. 進階版：可指定 key 做「去重依據」
def dedupe2(items, key=None):
    seen = set()
    for item in items:
        # 如果有 key，先算出比較用的值
        val = item if key is None else key(item)
        if val not in seen:
            yield item
            seen.add(val)
