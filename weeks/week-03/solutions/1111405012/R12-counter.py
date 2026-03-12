# R12. Counter 統計 + most_common（1.12）

from collections import Counter

# 1. Counter 用來做次數統計（像是字典但值是次數）
words = ["look", "into", "my", "eyes", "look"]
word_counts = Counter(words)
# 取出出現次數最多的前 3 個
word_counts.most_common(3)

# 2. update 可以再累加新的資料
word_counts.update(["eyes", "eyes"])
