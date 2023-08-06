# -*- coding: utf-8 -*-
# @Time    : 2021/10/3 10:33 上午
# @Author  : jeffery
# @FileName: search.py
# @website : http://www.jeffery.ink/
# @github  : https://github.com/jeffery0628
# @Description:


from typing import *


# --------------------------------------------- binary - search -------------------------------------------------------

def binary_search(nums: List[int], target: int) -> int:
    """
    在有序数组nums中搜索target
    Args:
        nums: 有序数组
        target: 要搜索的目标

    Returns:
        -1 : 表示在有序数组nums中未找到target
        0-(len(nums)-1):表示搜索目标的下标
    """
    left = 0
    right = len(nums) - 1

    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] < target:
            left = mid + 1
        elif nums[mid] > target:
            right = mid - 1
        elif nums[mid] == target:
            return mid
    return -1


def binary_search_left(nums: List[int], target: int) -> int:
    """
    在有序数组nums中搜索target，如果数组中存在多个targe，返回最左边的下标
    Args:
        nums: 有序数组
        target: 要搜索的目标

    Returns:
        -1 : 表示在有序数组nums中未找到target
        0-(len(nums)-1):表示搜索目标的下标
    """
    left = 0
    right = len(nums) - 1

    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] < target:
            left = mid + 1
        elif nums[mid] > target:
            right = mid - 1
        elif nums[mid] == target:  # 向左边界搜索,用right
            right = mid - 1

    if left >= len(nums) or not nums[left] == target:
        return -1
    return left


def binary_search_right(nums: List[int], target: int) -> int:
    """
    在有序数组nums中搜索target，如果数组中存在多个targe，返回最右边的下标
    Args:
        nums: 有序数组
        target: 要搜索的目标

    Returns:
        -1 : 表示在有序数组nums中未找到target
        0-(len(nums)-1):表示搜索目标的下标
    """
    left = 0
    right = len(nums) - 1
    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] < target:
            left = mid + 1
        elif nums[mid] > target:
            right = mid - 1
        elif nums[mid] == target:
            # 向右边界搜索，用left
            left = mid + 1
    if right < 0 or not nums[right] == target:
        return -1
    return right


# ---------------------------------------------- binary - insert -----------------------------------------------------
def binary_insert(nums: List[int], target: int) -> List[int]:
    left = 0
    right = len(nums) - 1
    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] < target:
            left = mid + 1
        elif nums[mid] > target:
            right = mid - 1
        elif nums[mid] == target:
            nums.insert(mid, target)
            break
    else:
        nums.insert(left, target)
    return nums


def binary_insert_left(nums: List[int], target: int) -> List[int]:
    """
    在有序数组nums中插入target，如果数组中存在多个targe，插入最左边的下标
    Args:
        nums: 有序数组
        target: 要插入的目标

    Returns:
        nums:插入target后的有序数组
    """
    left = 0
    right = len(nums) - 1
    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] < target:
            left = mid + 1
        elif nums[mid] > target:
            right = mid - 1
        elif nums[mid] == target:
            right = mid - 1
    nums.insert(left, target)
    return nums


def binary_insert_right(nums: List[int], target: int) -> List[int]:
    """
    在有序数组nums中插入target，如果数组中存在多个targe，插入最右边的下标
    Args:
        nums: 有序数组
        target: 要插入的目标

    Returns:
        nums:插入target后的有序数组
    """
    left = 0
    right = len(nums) - 1
    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] < target:
            left = mid + 1
        elif nums[mid] > target:
            right = mid - 1
        elif nums[mid] == target:
            left = mid + 1
    nums.insert(right, target)
    return nums


# ---------------------------------------------- bfs - search -----------------------------------------------------

def bfs_tree(root: List):
    if not root:
        return []

    queue = [root]
    result = []
    level = 0
    while queue:
        node = queue.pop(0)
        result.append((node.val, level))
        for sub_node in node.children():
            queue.append(sub_node)
        level += 1
    return result


