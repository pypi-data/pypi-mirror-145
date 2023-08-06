# -*- coding: utf-8 -*-
# @Time    : 2021/9/15 6:30 下午
# @Author  : jeffery
# @FileName: union_find.py
# @website : http://www.jeffery.ink/
# @github  : https://github.com/jeffery0628
# @Description: 并查集


class UnionFind:

    def __init__(self, n: int):
        """

        :param n: 最初的连通分量
        """
        self.count = n  # 用于返回连通分量个数
        self.root = [0]  # root表示存储每个节点的根节点，第一个位置用0占位
        self.size = [0]  # 用于存储树的深度

        for i in range(1, n + 1):
            self.root.append(i)  # 初始化所有节点都指向自身
            self.size.append(1)  # 初始化所有节点深度为1

    def find(self, p):
        """
        查找p节点的根节点

        注：在这里可以进行路径压缩优化,这样每次查询p，都可以减少p的搜索路径长度，节点查询越频繁，搜索路径越短，最短可优化至O(1)
        Args:
            p: p节点

        Returns:
            返回p节点的根节点
        """
        while not p == self.root[p]:
            self.root[p] = self.root[self.root[p]]  # 路径压缩优化
            p = self.root[p]
        return p

    def union(self, p, q) -> None:
        """
        将节点p和q进行连接
        注:可利用平衡树优化
        Args:
            p: p节点
            q: q节点

        Returns:
        """
        # 如果两节点连通，则不需要再进行连接操作
        root_p = self.find(p)
        root_q = self.find(q)
        if root_p == root_q:
            return
        # 利用点数类平衡树优化
        if self.size[root_p] > self.size[root_q]:
            root_p, root_q = root_q, root_p
        self.root[root_p] = root_q
        self.size[root_q] += self.size[root_q]
        self.count -= 1

    def is_connect(self, p, q) -> bool:
        """
        判断p、q两个节点是否连通,如果p、q两节点连通,则p、q两节点的根节点应该相同
        Args:
            p: p节点
            q: q节点

        Returns:
            返回bool类型，连通返回True，否则False
        """
        return self.find(p) == self.find(q)

    def count(self) -> int:
        """

        Returns:
            int : 返回当前的连通分量
        """
        return self.count
