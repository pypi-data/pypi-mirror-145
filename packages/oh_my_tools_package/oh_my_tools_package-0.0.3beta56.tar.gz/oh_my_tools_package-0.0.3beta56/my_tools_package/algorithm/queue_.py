# -*- coding: utf-8 -*-
# @Time    : 2021/9/25 7:07 下午
# @Author  : jeffery
# @FileName: queue_.py
# @website : http://www.jeffery.ink/
# @github  : https://github.com/jeffery0628
# @Description:

from collections import deque
import heapq
import queue


class PriorityQueue:
    """
    优先队列的实现：
    每次 pop 操作总是返回优先级最高的那个元素，如果两个元素优先级相同，按照被插入到队列的顺序返回
    """
    def __init__(self):
        self._queue = []
        self._index = 0

    def push(self, item, priority):
        """

        Args:
            item:  插入元素
            priority: 优先级

        """
        heapq.heappush(self._queue, (-priority, self._index, item))
        self._index += 1

    def pop(self):
        return heapq.heappop(self._queue)[-1]
