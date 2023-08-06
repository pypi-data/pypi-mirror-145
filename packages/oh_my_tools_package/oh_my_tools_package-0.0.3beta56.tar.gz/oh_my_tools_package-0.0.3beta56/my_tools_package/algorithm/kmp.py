# -*- coding: utf-8 -*-
# @Time    : 2021/9/30 12:10 上午
# @Author  : jeffery
# @FileName: kmp.py
# @website : http://www.jeffery.ink/
# @github  : https://github.com/jeffery0628
# @Description:  https://segmentfault.com/a/1190000038669408
from typing import *


def kmp_next(pattern: str) -> List[int]:
    # 创建一个next数组保存部分匹配值
    next_arr = [0] * len(pattern)

    j = 0
    for i in range(1, len(pattern)):
        while j > 0 and not pattern[i] == pattern[j]:
            j = next_arr[j - 1]

        if pattern[i] == pattern[j]:
            j += 1
        next_arr[i] = j
    return next_arr


def kmp_search(s: str, pattern: str) -> int:
    """
    在字符串s中查找字符串pattern首次匹配上的位置
    Args:
        s:
        pattern:

    Returns:

    """
    pattern_next = kmp_next(pattern)
    pattern_len = len(pattern)
    j = 0  # j指向模式串 pattern, i 指向 s 串
    for i in range(len(s)):
        while j > 0 and not s[i] == pattern[j]:  # 不相等的情况下基于next向前找
            j = pattern_next[j - 1]

        if s[i] == pattern[j]:
            j += 1
        if j == pattern_len:
            return i - j + 1

    return -1
