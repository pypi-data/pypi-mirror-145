# -*- coding: utf-8 -*-
# @Time    : 2021/10/3 5:03 下午
# @Author  : jeffery
# @FileName: backpack.py
# @website : http://www.jeffery.ink/
# @github  : https://github.com/jeffery0628
# @Description:


def zero_one_backpack(things, N, V):
    """
    定义一个二阶矩阵dp[N+1][V+1],
    这里之所以要N+1和V+1，是因为第0行表示只能选择第0个物品的时候，即没有物品的时候
    第0列表示背包的体积为0的时候，即不能装任何东西的时候

    dp[i][j]表示在 只能选择前i个物品，背包容量为j的情况下，背包中物品的最大价值
    对于dp[i][j]有两种情况：(对于当前物品i，要么选，要么不选)
    1. 不选择当前的第i件物品/第i件物品比背包容量要大，则dp[i][j] = dp[i-1][j]
    2. 选择当前的第i件物品（潜在要求第i件物品体积小于等于背包总容量），则能装入的物品最大价值为：
        当前物品的价值 加上 背包剩余容量在只能选前i-1件物品的情况下的最大价值
        dp[i][j] = dp[i-1][j-v[i]] + w[i]
    dp[i][j]在两种情况中选择比较大的情况作为当前的最优解；

    :param things:
    :param v:
    :return:
    """

    dp = [[0] * (V + 1) for _ in range(N + 1)]  # dp[N+1][V+1]
    for i in range(1, N + 1):
        for j in range(0, V + 1):
            if j >= things[i - 1][0]:
                dp[i][j] = max(dp[i - 1][j], dp[i - 1][j - things[i - 1][0]] + things[i - 1][1])
            else:
                dp[i][j] = dp[i - 1][j]
    return max(dp[N])





def zero_one_backpack_pro(things, N, V):
    """
    注意，这里第二层循环的时候，还是小到大循环的话，那么

    dp[i][j] = Math.max(dp[i-1][j], dp[i-1][j-v[i]] + w[i])
    实际上变成了
    dp[i][j] = Math.max(dp[i][j], dp[i][j-v[i]] + w[i]);

    因为i-1的值已经在前面被更新过了，覆盖了
    为了避免这个问题，所以要逆序更新，即先更新第i个，然后更新第i-1个，从而保证第i-1个不被覆盖

    :param things:
    :param N:
    :param V:
    :return:
    """
    dp = [0] * (V + 1)  # dp[V+1]
    for i in range(1, N + 1):
        for j in range(V, things[i - 1][0] - 1, -1):
            dp[j] = max(dp[j], dp[j - things[i - 1][0]] + things[i - 1][1])
    return max(dp)


def complete_pack(things, N, V):
    """
    因为可以重复选，不要求上一时刻的状态一定是上一个物品
    :param things:
    :param N:
    :param V:
    :return:
    """
    dp = [0] * (V + 1)
    for i in range(1, N + 1):
        for j in range(things[i - 1][0], V + 1):  # 注意：这里是顺序
            dp[j] = max(dp[j], dp[j - things[i - 1][0]] + things[i - 1][1])
    return max(dp)




def multi_pack_base(things, N, V):
    """

    :param things:
    :param N:
    :param V:
    :return:
    """
    dp = [0] * (V + 1)
    for i in range(1, N + 1):
        for j in range(V, things[i - 1][0] - 1, -1):  # 注意：这里又变成了逆序
            for k in range(0, things[i - 1][2] + 1):
                if k * things[i - 1][0] <= j:
                    dp[j] = max(dp[j], dp[j - k * things[i - 1][0]] + k * things[i - 1][1])
    return dp[V]


def multi_pack_pro(things, N, V):
    """

    :param things:
    :param N:
    :param V:
    :return:
    """
    changed_things = []
    for item in things:
        k = 1
        s = item[2]
        while k <= s:
            s -= k
            changed_things.append([k * item[0], k * item[1]])
            k *= 2
        if s > 0:
            changed_things.append([s * item[0], s * item[1]])
    print(changed_things)
    dp = [0] * (V + 1)

    for i in range(1, len(changed_things) + 1):
        for j in range(V, changed_things[i - 1][0] - 1, -1):
            if j >= changed_things[i - 1][0]:
                dp[j] = max(dp[j], dp[j - changed_things[i - 1][0]] + changed_things[i - 1][1])
    return max(dp)
