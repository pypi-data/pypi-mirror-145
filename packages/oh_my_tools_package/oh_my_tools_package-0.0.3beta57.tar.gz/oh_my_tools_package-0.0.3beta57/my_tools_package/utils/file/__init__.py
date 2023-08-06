# -*- coding: utf-8 -*-
# @Time    : 2021/8/25 8:51 上午
# @Author  : jeffery
# @FileName: __init__.py.py
# @website : http://www.jeffery.ink/
# @github  : https://github.com/jeffery0628
# @Description:

from my_tools_package.utils.file.file_utils import *
from my_tools_package.utils.file.file_reader import *
from my_tools_package.utils.file.file_writer import *


class IOUtils:

    @classmethod
    def write_yaml(cls,content,infile):
        return write_yaml(content,infile)


    @classmethod
    def read_json(cls, infile, encoding='utf8'):
        """
            读取json文件
        Args:
            infile: json 文件路径
            encoding: 默认utf8

        Returns:加载json文件后的dict

        """
        return read_json(infile, encoding)

    @classmethod
    def read_jsonl_list(cls, file_path: Union[str, Path], encoding: str = 'utf-8', fields: List[str] = None,
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
        return read_jsonl_list(file_path, encoding, fields, dropna)

    @classmethod
    def read_jsonl_generator(cls, file_path: Union[str, Path], encoding: str = 'utf-8', fields: List[str] = None,
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
        return read_jsonl_generator(file_path, encoding, fields, dropna)

    @classmethod
    def read_yaml(cls, infile, encoding='utf8'):
        """
        读取yaml格式的文件
        Args:
            infile: 配置文件路径
            encoding: 默认utf8

        Returns:返回字典格式的配置

        """
        return read_yaml(infile, encoding)

    @classmethod
    def untar_gz_file(cls, file: Path, to: Path):
        """
        解压缩tar.gz 文件
        :param file: 压缩文件路径
        :param to: 解压缩文件路径
        :return:
        """
        untar_gz_file(file, to)

    @classmethod
    def ungzip_file(cls, gzip_file: str, target_dir: Union[str, Path], target_filename: str) -> None:
        """
        解压缩gzip文件
        :param gzip_file: gzip文件路径
        :param target_dir: 解压到的文件夹
        :param target_filename: 文件名称
        :return:
        """

        ungzip_file(gzip_file, target_dir, target_filename)

    @classmethod
    def unbz2_file(cls, bz2_file: str, target_dir: Union[str, Path], target_filename: str) -> None:
        """
        解压缩bz2文件
        :param bz2_file: bz2文件路径
        :param target_dir: 解压到的文件夹
        :param target_filename: 文件名称
        :return:
        """
        unbz2_file(bz2_file, target_dir, target_filename)

    @classmethod
    def unzip_file(cls, file: Path, to: Path) -> None:
        """
        解压缩zip文件
        :param file: zip压缩文件路径
        :param to: 解压缩路径
        :return: None
        """
        unzip_file(file, to)

    @classmethod
    def ensure_dir(cls, dirname: Union[str, Path]) -> Path:
        """
        ensure dir path is exist,if not exist,make it
        Args:
            dirname: 文件夹 路径

        Returns:
        """
        return ensure_dir(dirname)

    @classmethod
    def ensure_file(cls, file_name: Union[str, Path]) -> Path:
        """
        ensure file path is exist,if not exist,make it
        Args:
            file_name: 文件路径
        Returns:
        """

        return ensure_file(file_name)

    @classmethod
    def copy_dir(cls, src: Union[Path, str], target: Union[Path, str]) -> None:
        """
        copy 文件夹的函数，递归的复制src下的文件及文件结构到target下
        Args:
            src: 源文件加
            target: 目标文件夹(可不存在)
        """
        copy_dir(src, target)
        gettempdir()



