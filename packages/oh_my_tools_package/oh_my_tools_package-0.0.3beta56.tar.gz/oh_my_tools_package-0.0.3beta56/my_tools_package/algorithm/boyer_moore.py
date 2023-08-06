# -*- coding: utf-8 -*-
# @Time    : 2021/10/3 9:35 下午
# @Author  : jeffery
# @FileName: boyer_moore.py
# @website : http://www.jeffery.ink/
# @github  : https://github.com/jeffery0628
# @Description:
# 参考：
# https://www.ruanyifeng.com/blog/2013/05/boyer-moore_string_search_algorithm.html
# https://github.com/NoserQjh/Boyer_Moore/blob/master/main.py
from typing import *


def generate_bad_character(pattern: str) -> Dict[str, int]:
    # 预生成坏字符表
    bad_characters_dict = dict()
    for i in range(len(pattern) - 1):
        char = pattern[i]
        # 记录坏字符最右位置（不包括模式串最右侧字符）
        bad_characters_dict[char] = i + 1
    return bad_characters_dict


def generate_good_suffix(pattern: str):
    # 预生成好后缀表
    good_suffix_dict = dict()
    pattern_len = len(pattern)

    # 无后缀仅根据坏字移位符规则
    good_suffix_dict[''] = 0

    for i in range(len(pattern)):
        # 好后缀 (从后向前)
        good_suffix_tail = pattern[pattern_len - i - 1:]
        for j in range(pattern_len - i - 1):
            # 匹配部分
            good_suffix_head = pattern[j:j + i + 1]

            # 记录模式串中好后缀最靠右位置（除结尾处）
            if good_suffix_tail == good_suffix_head:
                good_suffix_dict[good_suffix_tail] = pattern_len - j - i - 1
    return good_suffix_dict


def boyer_moore(text: str, pattern: str) -> List[Tuple[int,int]]:
    result = []

    pattern_len = len(pattern)
    text_len = len(text)
    if pattern_len <= 1:
        for idx,char in enumerate(text):
            if char == pattern:
                result.append((idx,idx+pattern_len))
        return result


    # 坏字符
    bad_character = generate_bad_character(pattern)
    # 好后缀
    good_suffix = generate_good_suffix(pattern)

    # 匹配过程
    i = 0
    j = pattern_len
    while i < text_len and j > 0:
        # 主串判断匹配部分
        text_char = text[i + j - 1:i + pattern_len]
        # 模式串判断匹配部分
        pattern_char = pattern[j - 1:]
        # 当前位匹配成功则继续匹配
        if text_char == pattern_char:
            j = j - 1
        # 当前位匹配失败根据规则移位
        else:
            if i + j - 1 >= text_len:
                return result
            i = i + max(good_suffix.setdefault(pattern_char[1:], pattern_len),
                        j - bad_character.setdefault(text[i + j - 1], 0))
            j = pattern_len

        # 匹配成功返回匹配位置
        if j == 0:
            result.append((i, i + pattern_len))
            if i + j - 1 >= text_len:
                return result
            i = i + max(good_suffix.setdefault(pattern_char[1:], pattern_len),
                        j - bad_character.setdefault(text[i + j - 1], 0))
            j = pattern_len
    return result

