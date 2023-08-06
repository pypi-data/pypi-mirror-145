# -*- coding: utf-8 -*-
# @Time    : 2021/8/25 8:52 上午
# @Author  : jeffery
# @FileName: file_reader.py
# @website : http://www.jeffery.ink/
# @github  : https://github.com/jeffery0628
# @Description:

import yaml
import json
from typing import *
from pathlib import Path
from collections import OrderedDict


def read_json(infile, encoding='utf8'):
    """
        读取json文件
    Args:
        infile: json 文件路径
        encoding:

    Returns:加载json文件后的dict

    """
    infile = Path(infile)
    with infile.open('rt', encoding=encoding) as handle:
        return json.load(handle, object_hook=OrderedDict)


def read_jsonl_list(file_path: Union[str, Path], encoding: str = 'utf-8', fields: List[str] = None,
                    dropna: bool = True) -> List[Dict]:
    """
    读取jsonl文件，并以列表的形式返回
    Args:
        file_path: jsonl 文件路径
        encoding: jsonl文件编码格式
        fields: 需要从json文件取出的键
        dropna: 如果键值不存在是否丢弃该数据

    Returns:以列表的形式返回读取内容

    """
    datas = []
    file_path = Path(file_path)
    if fields:
        fields = set(fields)

    with file_path.open("r", encoding=encoding) as f:
        for idx, line in enumerate(f):
            data = json.loads(line.strip())
            if fields is None:
                datas.append(data)
                continue
            _res = {}
            for k, v in data.items():
                if k in fields:
                    _res[k] = v
            if len(_res) < len(fields):
                if dropna:
                    continue
                else:
                    raise ValueError(f'invalid instance at line number: {idx}')
            datas.append(_res)
    return datas


def read_jsonl_generator(file_path: Union[str, Path], encoding: str = 'utf-8', fields: List[str] = None,
                         dropna: bool = True) -> Generator:
    """

    读取jsonl文件，并以列表的形式返回
    Args:
        file_path: jsonl 文件路径
        encoding: jsonl文件编码格式
        fields: 需要从json文件取出的键
        dropna: 如果键值不存在是否丢弃该数据

    Returns:以生成器的形式返回读取内容
    """

    file_path = Path(file_path)
    if fields:
        fields = set(fields)
    with file_path.open("r", encoding=encoding) as f:
        for idx, line in enumerate(f):
            data = json.loads(line.strip())
            if fields is None:
                yield idx, data
                continue
            _res = {}
            for k, v in data.items():
                if k in fields:
                    _res[k] = v
            if len(_res) < len(fields):
                if dropna:
                    continue
                else:
                    raise ValueError(f'invalid instance at line number: {idx}')
            yield idx, _res


def read_yaml(infile, encoding='utf8'):
    """
    读取yaml格式的文件
    Args:
        infile: 配置文件路径
        encoding: 默认utf8

    Returns:返回字典格式的配置

    """
    infile = Path(infile)
    with infile.open('r', encoding=encoding) as handle:
        return yaml.load(handle, Loader=yaml.Loader)

