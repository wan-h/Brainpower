# coding: utf-8
# Author: wanhui0729@gmail.com

import heapq

heap = [1, 3, 2, 7, 5]

# 将list x 转换成堆，原地，线性时间内
# heapq.heapify(heap)

# 将 item 的值加入 heap 中，保持堆的不变性。
heapq.heappush(heap, 4)

# 弹出并返回 heap 的最小的元素，保持堆的不变性。
# 如果堆为空，抛出 IndexError 。使用 heap[0] ，可以只访问最小的元素而不弹出它。
heap_min = heap[0]
heap_min_pop = heapq.heappop(heap)
print(heap_min, heap_min_pop)

# 将 item 放入堆中，然后弹出并返回 heap 的最小元素。
# 该组合操作比先调用  heappush() 再调用 heappop() 运行起来更有效率
heap_min_pop_push = heapq.heappushpop(heap, 6)
print(heap_min_pop_push)

# 弹出并返回 heap 中最小的一项，同时推入新的 item。 堆的大小不变。 如果堆为空则引发 IndexError。
# 这个单步骤操作比 heappop() 加 heappush() 更高效，并且在使用固定大小的堆时更为适宜。
heap_replace = heapq.heapreplace(heap, 7)
print(heap_replace)