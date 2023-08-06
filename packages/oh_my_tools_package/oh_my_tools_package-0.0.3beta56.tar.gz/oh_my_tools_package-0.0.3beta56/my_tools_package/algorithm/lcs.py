# -*- coding: utf-8 -*-
# @Time    : 2021/9/26 11:35 下午
# @Author  : jeffery
# @FileName: lcs.py
# @website : http://www.jeffery.ink/
# @github  : https://github.com/jeffery0628
# @Description:

from typing import *


def lcs_dp(text1: str, text2: str, continuous: bool = False) -> Tuple[List[List[int]], int]:
    """
    给定两个字符串 text1 和 text2，返回这两个字符串的 最长公共子序列 的长度。

    Args:
        text1: 字符串1
        text2: 字符串2
        continuous: 是否要求最长公共子序列连续
    Returns:
        返回一个整型，表示 字符串text1 和 字符串text2 的公共子序列的最大长度
    """

    m, n = len(text1), len(text2)
    # m 行 n 列
    dp = [[0 for _ in range(n + 1)] for _ in range(m + 1)]
    max_common_len = 0

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
                max_common_len = max(max_common_len, dp[i][j])
            else:
                if continuous:
                    dp[i][j] = 0
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp, max_common_len


def lcs_length(text1: str, text2: str, continuous: bool = False) -> int:
    """
    给定两个字符串 text1 和 text2，返回这两个字符串的 最长公共子序列 的长度。
    Args:
        text1: 字符串1
        text2: 字符串2
        continuous: 是否要求最长公共子序列连续
    Returns:
        返回一个整型，表示 字符串text1 和 字符串text2 的公共子序列的最大长度
    """
    dp, max_len = lcs_dp(text1, text2, continuous=continuous)
    return max_len


def lcs_string(text1: str, text2: str, continuous: bool = False) -> str:
    """

    Args:
        text1: 字符串1
        text2: 字符串2
        continuous: 是否要求最长公共子序列连续
    Returns:
        返回一个字符串，表示 字符串text1 和 字符串text2 的公共子序列
    """
    return _lcs_string_continuous(text1, text2) if continuous else _lcs_string(text1, text2)


def lcs_strings(text1: str, text2: str, continuous: bool = False) -> List[str]:
    return _lcs_strings_continuous(text1, text2) if continuous else _lcs_strings(text1, text2)


def _lcs_string_continuous(text1: str, text2: str) -> str:
    return _lcs_strings_continuous(text1, text2)[0]


def _lcs_strings_continuous(text1: str, text2: str) -> List[str]:
    dp, max_common_len = lcs_dp(text1, text2, continuous=True)
    # 公共子序列
    end_index = []
    for i in range(1, len(text1) + 1):
        for j in range(1, len(text2) + 1):
            if dp[i][j] == max_common_len:
                end_index.append(i)
    result = set()
    for idx in end_index:
        result.add(text1[idx - max_common_len:idx])
    return list(result)


def _lcs_string(text1: str, text2: str) -> str:
    """
        两个字符串的最长公共子序列很可能不唯一，输出其中一个最长公共子序列 (不连续)。

        思路：需要在动态规划表上进行回溯 —— dp[m][n]，即右下角的格子，开始进行判断：
            ①如果dp[i][j]对应的text1[i-1] == text2[j-1]，则把这个字符放入 结果集合 中，并跳入dp[i-1][j-1]中继续进行判断；

            ②如果格子dp[i][j]对应的 text1[i-1] ≠ text2[j-1]，则比较dp[i-1][j]和dp[i][j-1]的值，跳入值较大的格子继续进行判断；
            直到 i 或 j 小于等于零为止，倒序输出 LCS 。

            ③如果出现table[i-1][j]等于table[i][j-1]的情况，说明最长公共子序列有多个，故两边都要进行回溯（这里用到递归）。

        Args:
            text1: 字符串1
            text2: 字符串2

        Returns:
            common_str:最长公共子序列
    """
    dp, max_common_len = lcs_dp(text1, text2, continuous=False)
    # 公共子序列
    common_str = ""
    index_text1 = len(text1)
    index_text2 = len(text2)

    while index_text2 > 0:
        if index_text1 <= 0:
            break
        if dp[index_text1][index_text2] == max_common_len:
            if text1[index_text1 - 1] == text2[index_text2 - 1]:
                common_str = text1[index_text1 - 1] + common_str
                max_common_len -= 1
                index_text1 -= 1
                index_text2 -= 1
            else:
                index_text2 -= 1
        else:
            # 如果在 index_str1这行没找到， 公共元素，说明索引index_str1对应的元素不是公共元素， index_str1减一。
            index_text1 -= 1
            index_text2 += 1

    return common_str


def _lcs_strings(text1: str, text2: str) -> List[str]:
    """
    两个字符串的最长公共子序列很可能不唯一，输出所有最长公共子序列 (不连续)。

    思路：需要在动态规划表上进行回溯 —— dp[m][n]，即右下角的格子，开始进行判断：
        ①如果dp[i][j]对应的text1[i-1] == text2[j-1]，则把这个字符放入 结果集合 中，并跳入dp[i-1][j-1]中继续进行判断；

        ②如果格子dp[i][j]对应的 text1[i-1] ≠ text2[j-1]，则比较dp[i-1][j]和dp[i][j-1]的值，跳入值较大的格子继续进行判断；
        直到 i 或 j 小于等于零为止，倒序输出 LCS 。

        ③如果出现table[i-1][j]等于table[i][j-1]的情况，说明最长公共子序列有多个，故两边都要进行回溯（这里用到递归）。

    Args:
        text1: 字符串1
        text2: 字符串2

    Returns:

    """
    result = set()
    dp, max_len = lcs_dp(text1, text2, continuous=False)
    trace_back(dp, text1, text2, len(text1), len(text2), result, "")
    return list(result)


def trace_back(dp: List[List[int]], text1: str, text2: str, i: int, j: int, result: Set[str], temp):
    while i > 0 and j > 0:
        if text1[i - 1] == text2[j - 1]:
            temp = text1[i - 1] + temp
            i -= 1
            j -= 1
        else:
            if dp[i - 1][j] > dp[i][j - 1]:
                i -= 1
            elif dp[i - 1][j] < dp[i][j - 1]:
                j -= 1
            else:
                trace_back(dp, text1, text2, i - 1, j, result, temp)
                trace_back(dp, text1, text2, i, j - 1, result, temp)
                return
    result.add(temp)





