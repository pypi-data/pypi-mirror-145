# -*- coding: utf-8 -*-
# @Time    : 2021/8/25 8:55 上午
# @Author  : jeffery
# @FileName: file_writer.py
# @website : http://www.jeffery.ink/
# @github  : https://github.com/jeffery0628
# @Description:

import yaml
import json
from pathlib import Path


def write_yaml(content, infile):
    infile = Path(infile)
    with infile.open('w', encoding='utf8') as handle:
        yaml.dump(content, handle,)


def write_json(content, infile):
    infile = Path(infile)
    with infile.open('wt') as handle:
        json.dump(content, handle, indent=4, sort_keys=False)


