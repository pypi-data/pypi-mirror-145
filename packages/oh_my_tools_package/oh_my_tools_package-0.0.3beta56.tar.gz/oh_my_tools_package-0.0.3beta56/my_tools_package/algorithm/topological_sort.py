# -*- coding: utf-8 -*-
# @Time    : 2021/10/3 5:02 下午
# @Author  : jeffery
# @FileName: topological_sort.py
# @website : http://www.jeffery.ink/
# @github  : https://github.com/jeffery0628
# @Description:


from typing import List, Dict
from collections import defaultdict


def deep_topological_sort(vertex_num: int, edges: List[List[int]]) -> List[int]:
    # 初始化邻接边
    adjacent_deges = defaultdict(list)
    visited = [-1] * vertex_num  # -1 表示未访问过，0表示正在访问，1，表示访问过
    res = []
    for (tail, pre) in edges:
        adjacent_deges[pre].append(tail)

    for vertex in range(vertex_num):
        if not dfs(vertex, visited, adjacent_deges, res):  # 如果存在环
            return []
    res.reverse()
    return res


def dfs(vertex: int, visited: List, adjacent_edges: Dict, res: List):
    if visited[vertex] == 0:  # 遇到子节点正在访问，表示遇到环，无法构成拓扑结构
        return False
    elif visited[vertex] == 1:  # 子节点访问过了
        return True

    visited[vertex] = 0  # 设置该节点状态为访问中

    for sub_vertex in adjacent_edges[vertex]:
        if not dfs(sub_vertex, visited, adjacent_edges, res):  # 存在环
            return False

    visited[vertex] = 1  # 设置该节点状态：访问过
    res.append(vertex)
    return True


# ************************广度优先搜索******************************
def level_topological_sort(num_vertex: int, edges: List[List[int]]) -> List[int]:
    queue_zero = []
    # 初始化邻接边
    adjacent_edges = defaultdict(list)
    # 初始化入度表
    indegree = defaultdict(int)
    for (tail, pre) in edges:
        indegree[tail] += 1
        adjacent_edges[pre].append(tail)
    # 把入度为零的节点加入队列
    for vertex in range(num_vertex):
        if indegree[vertex] == 0:
            queue_zero.append(vertex)

    res = []
    while queue_zero:
        vertex = queue_zero.pop(0)  # 弹出队首节点，加入排序列表，并将与其关联的子节点的入度减一，如果子节点出现入度为零的点，则加入队列
        res.append(vertex)
        for sub_vertex in adjacent_edges[vertex]:
            indegree[sub_vertex] -= 1
            if indegree[sub_vertex] == 0:
                queue_zero.append(sub_vertex)
    if len(res) == num_vertex:
        return res
    return []
