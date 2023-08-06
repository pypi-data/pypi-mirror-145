# -*- coding: utf-8 -*-
# @Time    : 2021/8/21 11:51 上午
# @Author  : jeffery
# @FileName: file_utils.py
# @website : http://www.jeffery.ink/
# @github  : https://github.com/jeffery0628
# @Description:

import os
import gzip
import bz2
from typing import *
from pathlib import Path
from tempfile import gettempdir


def copy_dir(src: Union[Path, str], target: Union[Path, str]) -> None:
    """
    copy 文件夹的函数，递归的复制src下的文件及文件结构到target下
    Args:
        src: 源文件加
        target: 目标文件夹(可不存在)

    """
    src = Path(src)
    target = Path(target)
    if not target.exists():
        target.mkdir()

    files = list(src.glob("*"))
    for source_file in files:
        target_file = target / source_file.name
        if source_file.is_file():
            target_file.write_bytes(source_file.read_bytes())
        else:
            copy_dir(source_file, target_file)


def ensure_dir(dirname: Union[str, Path]) -> Path:
    """
    ensure dir path is exist,if not exist,make it
    Args:
        dirname: 文件夹 路径

    Returns:
    """
    dirname = Path(dirname)
    if not dirname.is_dir():
        dirname.mkdir(parents=True, exist_ok=False)
    return dirname


def ensure_file(file_name: Union[str, Path]) -> Path:
    file_name = Path(file_name)
    ensure_dir(file_name.parent)
    if not file_name.exists():
        file_name.touch(exist_ok=False)
    return file_name


def get_filepath(filepath):
    r"""
    如果filepath为文件夹，
        如果内含多个文件, 返回filepath
        如果只有一个文件, 返回filepath + filename
    如果filepath为文件
        返回filepath
    :param str filepath: 路径
    :return:
    """
    if os.path.isdir(filepath):
        files = os.listdir(filepath)
        if len(files) == 1:
            return os.path.join(filepath, files[0])
        else:
            return filepath
    elif os.path.isfile(filepath):
        return filepath
    else:
        raise FileNotFoundError(f"{filepath} is not a valid file or directory.")


def unzip_file(file: Path, to: Path) -> None:
    """
    解压缩zip文件
    :param file: zip压缩文件路径
    :param to: 解压缩路径
    :return: None
    """
    # unpack and write out in CoNLL column-like format
    from zipfile import ZipFile
    file = Path(file)
    to = Path(to)

    with ZipFile(file, "r") as zipObj:
        # Extract all the contents of zip file in current directory
        zipObj.extractall(to)


def untar_gz_file(file: Path, to: Path):
    """
    解压缩tar.gz 文件
    :param file: 压缩文件路径
    :param to: 解压缩文件路径
    :return:
    """
    import tarfile
    file = Path(file)
    to = Path(to)

    with tarfile.open(file, 'r:gz') as tar:
        tar.extractall(to)


def ungzip_file(gzip_file: str, target_dir: Union[str, Path], target_filename: str) -> None:
    """
    解压缩gzip文件
    :param gzip_file: gzip文件路径
    :param target_dir: 解压到的文件夹
    :param target_filename: 文件名称
    :return:
    """
    target_dir = ensure_dir(target_dir)

    with gzip.GzipFile(gzip_file, "rb") as source_file, open(os.path.join(target_dir, target_filename),
                                                             "wb") as target_file:
        for data in iter(lambda: source_file.read(100 * 1024), b""):
            target_file.write(data)


def unbz2_file(bz2_file: str, target_dir: Union[str, Path], target_filename: str) -> None:
    """
    解压缩gzip文件
    :param bz2_file: bz2文件路径
    :param target_dir: 解压到的文件夹
    :param target_filename: 文件名称
    :return:
    """
    target_dir = ensure_dir(target_dir)
    with bz2.BZ2File(bz2_file, "rb") as source_file, open(os.path.join(target_dir, target_filename),
                                                          "wb") as target_file:
        for data in iter(lambda: source_file.read(100 * 1024), b""):
            target_file.write(data)


if __name__ == '__main__':
    # copy_file("/Users/lizhen/Downloads/NLP-Pytorch-Template", "/Users/lizhen/Downloads/NLP-Pytorch-Template_copy")
    print(gettempdir())  # /var/folders/vg/1rrrfv_561g4z7p3zplfd01m0000gn/T
