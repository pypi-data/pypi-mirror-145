# -*- coding: utf-8 -*-
# @Time    : 2021/11/6 9:48 上午
# @Author  : jeffery
# @FileName: performance_analyse.py
# @website : http://www.jeffery.ink/
# @github  : https://github.com/jeffery0628
# @Description:
import cProfile
import pstats


def do_cprofile(filename, do_prof=True, sort_key="tottime"):
    """
    用于性能分析的装饰器函数
    :param filename: 表示分析结果保存的文件路径和名称
    """

    def wrapper(func):
        def profiled_func(*args, **kwargs):
            # 获取环境变量表示
            if do_prof:
                profile = cProfile.Profile()
                ## 开启性能分析的对象
                profile.enable()
                result = func(*args, **kwargs)
                profile.disable()
                ## 默认按照总计用时排序
                ps = pstats.Stats(profile).sort_stats(sort_key)
                ps.dump_stats(filename)
            else:
                result = func(*args, **kwargs)
            return result

    return wrapper
