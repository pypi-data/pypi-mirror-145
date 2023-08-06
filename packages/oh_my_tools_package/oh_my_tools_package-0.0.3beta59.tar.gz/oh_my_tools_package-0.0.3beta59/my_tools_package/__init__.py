# -*- coding: utf-8 -*-
# @Time    : 2021/8/21 11:49 上午
# @Author  : jeffery
# @FileName: __init__.py.py
# @website : http://www.jeffery.ink/
# @github  : https://github.com/jeffery0628
# @Description:
import os
from pathlib import Path
from typing import *
import pkg_resources
from my_tools_package.utils.file import IOUtils

def init_config_templates(over_write: bool = False):
    """
    初始化 配置文件模板到 home目录下/.oh_my_tools/config_templates
    Args:
        over_write: 是否覆盖原配置文件
    """
    HOME_DIR = Path(os.environ['HOME'])
    templates_dir = pkg_resources.resource_filename('my_tools_package', 'configs/')
    target_dir = HOME_DIR / '.oh_my_tools' / "configs"
    if over_write or not target_dir.exists():
        IOUtils.copy_dir(templates_dir, target_dir)


def setup_config(over_write_config: bool = False) -> None:
    """
    pip 安装后 自动加载或者初始化配置文件
    Args:
        over_write_config: 默认值为False ，如果为True则会将 HOME/.oh_my_tools/config_templates 下的配置文件全部初始化
    Returns:

    """
    HOME_DIR = Path(os.environ['HOME'])
    # 生成/加载配置文件
    glob_config_file = IOUtils.ensure_dir(HOME_DIR / '.oh_my_tools') / 'config.yaml'
    init_config_templates(over_write_config)
    if not glob_config_file.exists():
        glob_config_file.touch()
    configs = IOUtils.read_yaml(glob_config_file)
    if not configs:
        # 初始化配置
        configs = {
            "data_dir": os.path.join(str(HOME_DIR), 'data'),
            "dictionary_dir": os.path.join(str(HOME_DIR), "data/dictionary"),
            "dictionary_config_file": os.path.join(str(HOME_DIR), ".oh_my_tools", "configs/dictionary_config.yaml"),
            "cos_download_dir": os.path.join(str(HOME_DIR), "data/cos_download")
        }
        IOUtils.write_yaml(configs, glob_config_file)

    return configs


def save_config(conf_content: Dict, conf_file_path=None) -> None:
    """
    更新保存 my_tools_package 的配置信息
    :param conf_content: (dict) my_tools_package 的配置信息，Dict
    :param conf_file_path: 文件保存路径
    :return: None
    """
    HOME_DIR = Path(os.environ['HOME'])
    if not conf_file_path:
        conf_file_path = IOUtils.ensure_dir(HOME_DIR / '.oh_my_tools') / 'config.yaml'
    IOUtils.write_yaml(conf_content, conf_file_path)


CONF = setup_config()
