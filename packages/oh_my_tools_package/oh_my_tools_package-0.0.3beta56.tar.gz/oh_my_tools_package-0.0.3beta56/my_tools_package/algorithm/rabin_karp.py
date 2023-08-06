# -*- coding: utf-8 -*-
# @Time    : 2021/10/4 4:37 下午
# @Author  : jeffery
# @FileName: rabin_karp.py
# @website : http://www.jeffery.ink/
# @github  : https://github.com/jeffery0628
# @Description: https://github.com/mccricardo/Rabin-Karp/blob/master/rabin_karp.py
# https://github.com/hansrajdas/algorithms/blob/master/Level-3/rabin_karp.py
from typing import *


def rehash(prev_hash: int, first: str, last: str, d: int) -> int:
    """Returns new hash if first char removed and last char is added."""
    return ((prev_hash - ord(first) * d) << 1) + ord(last)


def rabin_karp(text: str, pattern: str) -> List[Tuple[int, int]]:
    """Returns list of indices in text string which matches given pattern."""
    matches = []
    text_val = 0  # Hash of running text frame
    pattern_val = 0  # Hash of pattern
    text_len = len(text)
    pattern_len = len(pattern)

    if pattern_len > text_len or not pattern or not text:
        return []

    d = 1 << pattern_len - 1
    for i in range(pattern_len):
        pattern_val = (pattern_val << 1) + ord(pattern[i])
        text_val = (text_val << 1) + ord(text[i])

    # Search
    j = 0
    while j <= text_len - pattern_len:
        if pattern_val == text_val and pattern == text[j:j + pattern_len]:
            matches.append((j, j + pattern_len))
        if j < text_len - pattern_len:
            text_val = rehash(text_val, text[j], text[j + pattern_len], d)
        j += 1
    return matches
