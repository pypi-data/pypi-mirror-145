# -*- coding: utf-8 -*-
# @Time    : 2021/9/27 8:33 上午
# @Author  : jeffery
# @FileName: levenshtein.py
# @website : http://www.jeffery.ink/
# @github  : https://github.com/jeffery0628
# @Description:


def levenshtein_distance(text1: str, text2: str) -> int:
    """
    levenshtein 编辑距离
    Args:
         text1: 字符串1
        text2: 字符串2

    Returns:
        返回一个整型，表示 字符串text1 和 字符串text2 的最小编辑距离
    """

    m, n = len(text1), len(text2)
    # m 行 n 列
    dp = [[0 for _ in range(n + 1)] for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])

    return dp[m][n]
