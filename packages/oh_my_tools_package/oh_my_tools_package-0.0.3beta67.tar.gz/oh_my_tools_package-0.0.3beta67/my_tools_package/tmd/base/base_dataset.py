# -*- coding: utf-8 -*-
# @Time    : 2022/4/4 1:08 下午
# @Author  : jeffery
# @FileName: base_dataset.py
# @github  : https://github.com/jeffery0628
# @Description:

import logging
import math
from dataclasses import dataclass

import torch
from pathlib import Path
from abc import ABCMeta, abstractmethod
from sklearn.model_selection import KFold
from my_tools_package.utils.file import IOUtils
from torch.utils.data.dataset import Dataset, IterableDataset
from typing import Union, Optional, List, Dict


@dataclass
class InputExample:
    guid: Optional[str]
    text: str
    labels: List[list]


@dataclass
class InputFeatures:
    guid: Optional[str]
    tfs_inputs: Dict
    text: str
    label: Dict


class BaseDataSet(IterableDataset, metaclass=ABCMeta):
    def __init__(self, feature_cache_file: Union[str, Path] = None, overwrite: bool = False):
        self.feature_cache_file = feature_cache_file

        # 如果缓存文件不存在或者重写缓存文件 否则直接加载缓存文件
        if not self.feature_cache_file.exists() or overwrite:
            self.features = self.save_features_to_cache()
        else:
            self.features = self.load_features_from_cache()

    @abstractmethod
    def read_examples_from_file(self):
        raise NotImplementedError

    @abstractmethod
    def convert_examples_to_features(self):
        raise NotImplementedError

    def save_features_to_cache(self):
        features = self.convert_examples_to_features()
        logging.info('saving feature to cache file : {}...'.format(self.feature_cache_file))
        IOUtils.ensure_file(self.feature_cache_file)
        torch.save(features, self.feature_cache_file)
        return features

    def load_features_from_cache(self):
        logging.info('loading features from cache file : {}...'.format(self.feature_cache_file))
        features = torch.load(self.feature_cache_file)
        return features

    def __len__(self):
        return len(self.features)

    def __getitem__(self, index):
        return self.features[index]

    def __iter__(self):
        worker_info = torch.utils.data.get_worker_info()
        start, end = 0, len(self.features)
        if worker_info is None:
            iter_start = start
            iter_end = end
        else:  # in a worker process
            worker_id = worker_info.id
            per_worker = int(math.ceil(((end - start) / float(worker_info.num_workers))))
            iter_start = start + worker_id * per_worker
            iter_end = min(iter_start + per_worker, end)
        return iter(self.features[iter_start:iter_end])

    def make_k_fold_data(self, k):
        """
        :param k:
        :return:
        """
        kf = KFold(n_splits=k)  # 分成几个组
        for i, (train_index, valid_index) in enumerate(kf.split(self.features)):
            yield i, train_index, valid_index
