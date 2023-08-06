# -*- coding: utf-8 -*-
# @Time    : 2021/10/3 10:15 上午
# @Author  : jeffery
# @FileName: backtrack.py
# @website : http://www.jeffery.ink/
# @github  : https://github.com/jeffery0628
# @Description:
#
#


from typing import *
from copy import deepcopy


def backtrack(results: List, path: List, arr: List):
    """
    回溯算法不可重复 每一层随着可选择的元素减少，arr的长度随着递归减小
    :param results: 结果集
    :param path: 回溯的路径
    :param arr: 原数组
    :return:
    """
    # 递归出口
    if len(arr) == 0:
        results.append(deepcopy(path))
        return

    for i in range(len(arr)):
        # 选择
        path.append(arr.pop(i))
        # 尝试
        backtrack(results, path, arr)
        # 回溯
        arr.insert(i, path.pop())


def backtrack_repeat(results: List, path: List, arr: List):
    """
    可重复:相当于每一层都有nums.length 个选择，arr的长度随着递归不发生变化
    :param results:
    :param path:
    :param arr:
    :return:
    """
    # 递归出口:满足条件
    if len(path) == len(arr):
        results.append(deepcopy(path))
        return

    for i in range(len(arr)):
        # 选择
        path.append(arr[i])
        # 尝试
        backtrack(results, path, arr)
        # 回溯
        path.pop()
