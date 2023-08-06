# -*- coding: utf-8 -*-
# @Time    : 2022/4/4 1:47 下午
# @Author  : jeffery
# @FileName: config_parser.py
# @github  : https://github.com/jeffery0628
# @Description:
import importlib.util
import json
import os
from functools import partial

import torch

from typing import Dict, Union
from pathlib import Path
from my_tools_package.utils.file import IOUtils
from my_tools_package.utils.logger import init_logger
from transformers import BertTokenizer, AutoTokenizer, AutoConfig, AutoModel
from torch.utils.data import dataloader as module_dataloader
import transformers.optimization as module_optimization

from my_tools_package.utils.torch import set_seed


class TMDDict(dict):
    __setattr__ = dict.__setitem__
    __getattr__ = dict.__getitem__

    def __hash__(self):
        hash(self)


class ConfigParser:

    def __init__(self, config={}):
        self.tmd_config = self.to_tmd_config(config)
        set_seed(self.tmd_config.seed)
        self.experiment_name = self.tmd_config.experiment_name
        self.logger = self.set_logger(self.tmd_config.log)
        self.tfs = self._set_transformers(self.tmd_config)
        self.device, self.device_ids = self._prepare_device(self.tmd_config.device)
        self.label2id, self.id2label = self.load_label_map(self.tmd_config.label_map_path)

    def train(self):
        # dataloader
        for i_fold, train_loader, valid_loader, test_loader in self.generate_dataloader(self.tmd_config.dataset):
            # model
            model = self._prepare_model(self.tmd_config.model)
            optimizer = self._prepare_optimizer(self.tmd_config.optimizer, model)
            lr_scheduler = self._prepare_lr_scheduler(self.tmd_config.lr_scheduler, train_loader, optimizer)
            criterions = self._prepare_criterions(self.tmd_config.loss)
            metrics = self._prepare_metrics(self.tmd_config.metrics)

            trainer = self._prepare_trainer(trainer_config=self.tmd_config.trainer, i_fold=i_fold, device=self.device,
                                            device_ids=self.device_ids, logger=self.logger, tmd_config=self.tmd_config,
                                            train_loader=train_loader, valid_loader=valid_loader,id2label=self.id2label,
                                            test_loader=test_loader, model=model, optimizer=optimizer,
                                            lr_scheduler=lr_scheduler, criterions=criterions, metrics=metrics)
            trainer.train()

    def _prepare_trainer(self, trainer_config, i_fold, device, device_ids, logger, tmd_config, train_loader,
                         valid_loader, test_loader, model, optimizer,id2label,
                         lr_scheduler, criterions, metrics):

        if trainer_config.module:
            module_spec = importlib.util.spec_from_file_location(trainer_config.type, trainer_config.module)
            trainer_module = importlib.util.module_from_spec(module_spec)
            module_spec.loader.exec_module(trainer_module)
        else:
            import my_tools_package.tmd.trainer.trainer as trainer_module

        trainer = self.init_obj(trainer_config.type, module_args=None, module=trainer_module, i_fold=i_fold,
                                device=device, device_ids=device_ids, train_loader=train_loader,id2label=id2label,
                                valid_loader=valid_loader, test_loader=test_loader, model=model, optimizer=optimizer,
                                lr_scheduler=lr_scheduler, logger=logger, tmd_config=tmd_config,
                                criterions=criterions, metric_ftns=metrics)
        return trainer

    def _prepare_metrics(self, metric_config):
        import my_tools_package.tmd.metric.ner as metric_module
        return [getattr(metric_module, met) for met in metric_config.type]

    def _prepare_criterions(self, loss_config):
        import my_tools_package.tmd.loss.loss as loss_module
        return [getattr(loss_module, crit) for crit in loss_config.type]

    def _prepare_lr_scheduler(self, scheduler_config, train_loader, optimizer):
        t_total = len(train_loader) * scheduler_config.epochs
        num_warmup_steps = int(scheduler_config.warmup_proportion * t_total)

        if 'cosine' in scheduler_config:
            lr_scheduler = self.init_obj(scheduler_config.type, scheduler_config.args, module_optimization, optimizer,
                                         num_warmup_steps=num_warmup_steps,
                                         num_training_steps=t_total,
                                         )
        else:
            lr_scheduler = self.init_obj(scheduler_config.type, scheduler_config.args, module_optimization, optimizer,
                                         num_warmup_steps=num_warmup_steps,
                                         num_training_steps=t_total,
                                         )

        return lr_scheduler

    def _prepare_optimizer(self, optimizer_config, model):

        module_spec = importlib.util.spec_from_file_location(optimizer_config.type, optimizer_config.module)
        optimizer_module = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(optimizer_module)

        optimizer = getattr(optimizer_module, optimizer_config.type)(model=model)
        return optimizer

    def load_label_map(self, label_map_path):
        with open(label_map_path, "r", encoding="utf8") as f:
            label_map = json.load(f)
        id2label = {}
        for idx,label in label_map["id2label"].items():
            id2label[int(idx)] = label
        return label_map["label2id"], id2label

    def generate_dataloader(self, dataset_config):
        module_spec = importlib.util.spec_from_file_location(dataset_config.type, dataset_config.module)
        data_module = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(data_module)
        test_set = self.init_obj(dataset_config.type, dataset_config.test_set_args, data_module,
                                 tokenizer=self.tfs.tokenizer, label2id=self.label2id, is_test=True)
        test_loader = module_dataloader.DataLoader(test_set, batch_size=test_set.batch_size * 2,
                                                   collate_fn=test_set.collate_fn)

        if dataset_config.k_fold > 0:
            self.logger.info(
                f"making {dataset_config.k_fold} fold data for file :{dataset_config.all_set_args.file_name}")
            all_set = self.init_obj(dataset_config.type, dataset_config.all_set_args, data_module,
                                    tokenizer=self.tfs.tokenizer, label2id=self.label2id)

            for i, train_index, valid_index in all_set.make_k_fold_data(dataset_config.k_fold):
                train_set = torch.utils.data.dataset.Subset(all_set, train_index)
                valid_set = torch.utils.data.dataset.Subset(all_set, valid_index)

                train_loader = module_dataloader.DataLoader(train_set, batch_size=all_set.batch_size,
                                                            collate_fn=all_set.collate_fn)
                valid_loader = module_dataloader.DataLoader(valid_set, batch_size=all_set.batch_size,
                                                            collate_fn=all_set.collate_fn)

                yield i, train_loader, valid_loader, test_loader
        else:
            train_set = self.init_obj(dataset_config.type, dataset_config.train_set_args, data_module,
                                      tokenizer=self.tfs.tokenizer, label2id=self.label2id)
            valid_set = self.init_obj(dataset_config.type, dataset_config.valid_set_args, data_module,
                                      tokenizer=self.tfs.tokenizer, label2id=self.label2id)

            train_loader = module_dataloader.DataLoader(train_set, batch_size=train_set.batch_size,
                                                        collate_fn=train_set.collate_fn)
            valid_loader = module_dataloader.DataLoader(valid_set, batch_size=valid_set.batch_size,
                                                        collate_fn=valid_set.collate_fn)
            yield 0, train_loader, valid_loader, test_loader

    def _prepare_model(self, model_config):
        if len(model_config.module) > 0:
            module_spec = importlib.util.spec_from_file_location(model_config.type, model_config.module)
            model_module = importlib.util.module_from_spec(module_spec)
            module_spec.loader.exec_module(model_module)
        else:
            import my_tools_package.tmd.model.model as model_module
        self.tfs.model.resize_token_embeddings(len(self.tfs.tokenizer))
        model = self.init_obj(model_config.type, model_config.args, model_module, tfs=self.tfs,
                              class_num=len(self.label2id))
        return model

    def set_logger(self, log_config):
        return init_logger(log_config.log_level, log_config.log_file, log_config.log_file_level)

    def _prepare_device(self, device_config):
        """
        setup GPU device if available, move model into configured device
        """
        if torch.cuda.is_available():
            os.environ["CUDA_VISIBLE_DEVICES"] = device_config.visual_device

        n_gpu = torch.cuda.device_count()
        n_gpu_use = device_config.num_gpu
        if n_gpu_use > 0 and n_gpu == 0:
            self.logger.warning("Warning: There\'s no GPU available on this machine,training will be performed on CPU.")
            n_gpu_use = 0

        if n_gpu_use > n_gpu:
            self.logger.warning(
                f"Warning: The number of GPU\'s configured to use is {n_gpu_use}, but only {n_gpu} are available "
                "on this machine.")
            n_gpu_use = n_gpu

        device = torch.device(f'cuda:{device_config.main_device_id}' if n_gpu_use > 0 else 'cpu')
        list_ids = device_config.device_ids
        return device, list_ids

    def _set_transformers(self, tmd_config):
        """
        设置transformers
        """
        if "tfs_name_or_path" not in tmd_config or len(tmd_config.tfs_name_or_path) == 0:
            return None

        tfs = TMDDict()
        tokenizer_kwargs = {
            "do_lower_case": tmd_config.tokenizer_do_lower_case,
        }
        tfs["config"] = AutoConfig.from_pretrained(tmd_config.tfs_name_or_path)
        tfs["model"] = AutoModel.from_pretrained(tmd_config.tfs_name_or_path)
        if "albert" in tmd_config.tfs_name_or_path.lower() or "roberta" in tmd_config.tfs_name_or_path.lower():
            tfs["tokenizer"] = BertTokenizer.from_pretrained(tmd_config.tfs_name_or_path, **tokenizer_kwargs)
        else:
            tfs["tokenizer"] = AutoTokenizer.from_pretrained(tmd_config.tfs_name_or_path, **tokenizer_kwargs)

        return tfs

    def to_tmd_config(self, config: dict):
        if not isinstance(config, dict):
            return config
        tmd_dict = TMDDict()
        for k, v in config.items():
            tmd_dict[k] = self.to_tmd_config(v)
        return tmd_dict

    def init_obj(self, cls_name, module_args, module, *args, **kwargs):
        """
        Finds a function handle with the name given as 'type' in config, and returns the
        instance initialized with corresponding arguments given.
        `object = config.init_obj('name', module, a, b=1)`
        is equivalent to
        `object = module.name(a, b=1)`
        """
        module_args = dict(module_args) if module_args else dict()
        assert all([k not in module_args for k in kwargs]), 'Overwriting kwargs given in config file is not allowed'
        module_args.update(kwargs)
        return getattr(module, cls_name)(*args, **module_args)

    def init_ftn(self, ftn_name, ftn_name_args, module, *args, **kwargs):
        """
        Finds a function handle with the name given as 'type' in config, and returns the
        function with given arguments fixed with functools.partial.
        `function = config.init_ftn('name', module, a, b=1)`
        is equivalent to
        `function = lambda *args, **kwargs: module.name(a, *args, b=1, **kwargs)`.
        """
        module_args = dict(ftn_name_args) if ftn_name_args else dict()
        assert all([k not in module_args for k in kwargs]), 'Overwriting kwargs given in config file is not allowed'
        module_args.update(kwargs)
        return partial(getattr(module, ftn_name), *args, **module_args)

    @classmethod
    def from_file(cls, cfg_file: Union[str, Path]):
        """
        从配置文件生成 模型训练配置
        Args:
            cfg_file: 配置文件路径
        Returns:
        """
        return cls(IOUtils.read_yaml(cfg_file))

    @classmethod
    def from_dict(cls, cur_config: Dict):
        return cls(cur_config)


