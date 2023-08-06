# -*- coding: utf-8 -*-
# @Time    : 2022/4/3 10:21 下午
# @Author  : jeffery
# @FileName: downloader.py
# @github  : https://github.com/jeffery0628
# @Description:

import os
import os.path
from transformers import AutoModel,BertTokenizer
from pathlib import Path
from typing import Union
from qcloud_cos import CosConfig, CosServiceError, CosS3Client
from my_tools_package import CONF
from my_tools_package.utils.file import IOUtils


class COSDownloader:
    cos_config = CosConfig(Region='ap-beijing', SecretId='AKIDthHeniPr42mHZdR1MRHqAbqtkNlvqWxB',
                           SecretKey='2pNfkdK2kHaeV8XhpnX4NSIuT1OWRAlg', Token=None, Scheme='https')
    cos_client = CosS3Client(cos_config)
    cos_download_dir = IOUtils.ensure_dir(CONF["cos_download_dir"])

    @classmethod
    def download_file(cls, bucket, file_key, save_dir: Union[str,Path] = None):
        save_path = IOUtils.ensure_dir(save_dir) if save_dir else cls.cos_download_dir
        file_path = save_path / file_key.split("/")[-1]
        if not file_path.exists():
            try:
                cls.cos_client.download_file(
                    Bucket=f'{bucket}',
                    Key=f'{file_key}',
                    DestFilePath=f'{file_path}'
                )
            except CosServiceError as e:
                print(e.args)
                return None
        return str(file_path)





def download_from_huggingface(model_name, root_path):
    """
    1. 下载可能会失败，重试即可
    2. 程序会缓存之前下载过的内容
    :param model_name: from https://huggingface.co/models,
        e.g. download_from_huggingface('uer/chinese_roberta_L-2_H-128', '/Users/lilin/Desktop/temp1')
    :param root_path:
    :return:
    """
    path = os.path.join(root_path, model_name)
    tokenizer = BertTokenizer.from_pretrained(model_name)
    tokenizer.save_pretrained(path)

    model = AutoModel.from_pretrained(model_name)
    model.save_pretrained(path)
    print(path, 'done.')


if __name__ == '__main__':
    download_from_huggingface('clue/albert_chinese_small',
                              '/data/lizhen/pretrained_models')
