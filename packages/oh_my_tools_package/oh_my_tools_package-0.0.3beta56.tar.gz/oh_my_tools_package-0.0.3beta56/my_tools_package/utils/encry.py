# -*- coding: utf-8 -*-
# @Time    : 2021/9/5 8:37 下午
# @Author  : jeffery
# @FileName: encry.py
# @website : http://www.jeffery.ink/
# @github  : https://github.com/jeffery0628
# @Description:

from hashlib import md5


def encry_md5(in_str: str, salt: str = "jeffery") -> str:
    """
    输入 字符串，对字符串采用md5算法加密，
    :param in_str:  需要加密的字符串
    :param salt:  盐，防止被撞库
    :return:  对字符串加密后的结果
    """

    obj = md5(salt.encode("utf8"))
    obj.update(in_str.encode("utf8"))
    return obj.hexdigest()
