# R5. 優先佇列 PriorityQueue（1.5）

# 用 heapq 實作最大優先（priority 越大越先出）
import heapq


class PriorityQueue:
    def __init__(self):
        # _queue 裡放的是 tuple：(-priority, index, item)
        # priority 取負號，讓 min-heap 表現成 max-heap
        self._queue = []
        # index 用來打破「優先度相同」的排序，保持先進先出
        self._index = 0

    def push(self, item, priority):
        heapq.heappush(self._queue, (-priority, self._index, item))
        self._index += 1

    def pop(self):
        # heappop 回傳 tuple，最後一個元素才是 item
        return heapq.heappop(self._queue)[-1]
