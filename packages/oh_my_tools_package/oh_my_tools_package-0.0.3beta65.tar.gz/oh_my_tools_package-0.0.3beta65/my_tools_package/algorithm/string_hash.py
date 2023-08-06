# -*- coding: utf-8 -*-
# @Time    : 2021/9/28 9:35 上午
# @Author  : jeffery
# @FileName: string_hash.py
# @website : http://www.jeffery.ink/
# @github  : https://github.com/jeffery0628
# @Description: 字符串hash

#  https://blog.csdn.net/yl2isoft/article/details/16362479


M = 249997  # 模
M1 = 1000001
M2 = 0xF0000000


def BKDRHash(s: str):
    seed = 131  # 31 131 1313 13131 131313 etc..
    hash_value = 0
    for char in s:
        hash_value = hash_value * seed + (ord(char))
    return hash_value % M




if __name__ == '__main__':
    print(BKDRHash("我 哎 中改"))
