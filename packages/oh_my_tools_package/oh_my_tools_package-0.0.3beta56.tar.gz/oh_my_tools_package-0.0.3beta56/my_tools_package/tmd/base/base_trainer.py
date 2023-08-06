# -*- coding: utf-8 -*-
# @Time    : 2022/4/4 1:42 下午
# @Author  : jeffery
# @FileName: base_trainer.py
# @github  : https://github.com/jeffery0628
# @Description:
from itertools import repeat
from pathlib import Path
import datetime
import torch
from abc import abstractmethod
from numpy import inf
from time import time
from my_tools_package.utils.torch import TensorboardWriter
from my_tools_package.utils.file import IOUtils


class BaseTrainer:
    """
    Base class for all trainers
    """

    def __init__(self, i_fold, device, device_ids, model, optimizer, criterions, metric_ftns, logger, tmd_config):
        self.tmd_config = tmd_config
        self.device = device
        self.device_ids = device_ids
        self.logger = logger
        self.model = torch.nn.DataParallel(model.to(self.device), device_ids=device_ids) if len(
            device_ids) > 1 else model.to(self.device)
        self.criterion = criterions
        self.metric_ftns = metric_ftns
        self.optimizer = optimizer
        self.i_fold = i_fold
        self.epochs = tmd_config.trainer.epochs
        self.inference = tmd_config.trainer.get("inference", False)
        self.save_period = tmd_config.trainer.get('save_period', 0)
        self.monitor = tmd_config.metrics.get('monitor', 'off')
        self.add_graph = tmd_config.trainer.get('add_graph', False)

        # configuration to monitor model performance and save best
        if self.monitor == 'off':
            self.mnt_mode = 'off'
            self.mnt_best = 0
        else:
            self.mnt_mode, self.mnt_metric = self.monitor.split()
            assert self.mnt_mode in ['min', 'max']
            self.mnt_best = inf if self.mnt_mode == 'min' else -inf
            self.early_stop = tmd_config.trainer.get('early_stop', inf)

        self.start_epoch = 1
        self.best_epoch = self.start_epoch
        self.checkpoint_dir = Path(
            tmd_config.trainer.save_dir) / f"{tmd_config.experiment_name}-{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"

        self.logger_dir = IOUtils.ensure_dir(self.checkpoint_dir / "log")
        self.result_dir = IOUtils.ensure_dir(self.checkpoint_dir / "result")
        self.model_dir = IOUtils.ensure_dir(self.checkpoint_dir / "model")
        self.diff_dir = IOUtils.ensure_dir(self.checkpoint_dir / "diff")

        # setup visualization writer instance
        self.writer = TensorboardWriter(self.logger_dir, self.logger, tmd_config.trainer.tensorboard)

        if tmd_config.trainer.resume_path is not None:
            self._resume_checkpoint(tmd_config.trainerresume_path)

        self.valid_diff = {}

    @abstractmethod
    def _train_epoch(self, epoch):
        """
        Training logic for an epoch
        Args:
            epoch: Current epoch number
        Returns:
        """
        raise NotImplementedError

    def _valid_epoch(self, epoch):
        raise NotImplementedError

    def _inference(self):
        raise NotImplementedError

    def train(self):
        """
        Full training logic
        """
        not_improved_count = 0
        for epoch in range(self.start_epoch, self.epochs + 1):
            t1 = time()
            result = self._train_epoch(epoch)
            # save logged informations into log dict
            log = {
                'spending time': (time() - t1),
                'epoch': epoch
            }
            log.update(result)

            # print logged informations to the screen
            for key, value in log.items():
                self.logger.info('    {:30s}: {}'.format(str(key), value))

            # evaluate model performance according to configured metric, save best checkpoint as model_best
            best = False
            if self.mnt_mode != 'off':
                try:
                    # check whether model performance improved or not, according to specified metric(mnt_metric)
                    improved = (self.mnt_mode == 'min' and log[self.mnt_metric] <= self.mnt_best) or \
                               (self.mnt_mode == 'max' and log[self.mnt_metric] >= self.mnt_best)
                except KeyError:
                    self.logger.warning(
                        f"Warning: Metric '{self.mnt_metric}' is not found. Model performance monitoring is disabled.")
                    self.mnt_mode = 'off'
                    improved = False

                if improved:
                    self.mnt_best = log[self.mnt_metric]
                    self.best_epoch = epoch
                    not_improved_count = 0
                    best = True
                else:
                    not_improved_count += 1

                if not_improved_count >= self.early_stop:
                    self.logger.info(
                        f'best epoch:{self.best_epoch},{self.mnt_mode} {self.mnt_metric}:{self.mnt_best}')

                    self.logger.info(
                        f"Validation performance didn\'t improve for {self.early_stop} epochs. Training stops.")

                    break

                self.logger.info(
                    'best epoch:{},{} {}:{}'.format(self.best_epoch, self.mnt_mode, self.mnt_metric, self.mnt_best))
            if best:
                self._save_best_checkpoint(epoch)

            if self.save_period > 0 and epoch % self.save_period == 0:
                self._save_checkpoint(epoch)
        if self.inference:
            self._inference()

    def _save_checkpoint(self, epoch):
        """
        Saving checkpoints
        Args:
            epoch: current epoch number
        Returns:
        """
        arch = type(self.model).__name__
        state = {
            'arch': arch,
            'epoch': epoch,
            'model': self.model.state_dict(),
            'optimizer': self.optimizer.state_dict(),
            'monitor_best': self.mnt_best,
        }
        filename = str(self.model_dir / f'checkpoint-epoch{epoch}.pth')
        torch.save(state, filename)
        self.logger.info(f"Saving checkpoint: {filename} ...")

    def _save_best_checkpoint(self, epoch):
        """
        Saving  best checkpoints
        Args:
            epoch: current epoch number
        Returns:
        """
        arch = type(self.model).__name__
        state = {
            'arch': arch,
            'epoch': epoch,
            'model': self.model.state_dict(),
            'optimizer': self.optimizer.state_dict(),
            'monitor_best': self.mnt_best,
        }
        self.best_path = str(self.checkpoint_dir / f"model_best_{self.i_fold}.pth")
        torch.save(state, self.best_path)
        self.logger.info(f"Saving current best: {self.best_path} ...")

    def _resume_checkpoint(self, resume_path, optimizer: bool = False):
        """
        Resume from saved checkpoints
        Args:
            resume_path:
        Returns:
        """
        resume_path = str(resume_path)
        self.logger.info(f"Loading checkpoint: {resume_path} ...")
        checkpoint = torch.load(resume_path)
        self.start_epoch = checkpoint['epoch'] + 1
        self.best_epoch = self.start_epoch
        self.mnt_best = checkpoint['monitor_best']

        # load architecture params from checkpoint.
        if checkpoint['arch'] != self.tmd_config.model_config.type:
            self.logger.warning("Warning: Architecture configuration given in config file is different from that of "
                                "checkpoint. This may yield an exception while state_dict is being loaded.")
        self.model.load_state_dict(checkpoint['state_dict'])
        self.optimizer.load_state_dict(checkpoint['optimizer'])
        self.logger.info(f"Checkpoint loaded. Resume from epoch {self.start_epoch - 1}")

    def inf_loop(self,data_loader):
        ''' wrapper function for endless data loader. '''
        for loader in repeat(data_loader):
            yield from loader

    def _progress(self, batch_idx):
        base = '[{}/{} ({:.0f}%)]'
        if hasattr(self.train_loader, 'n_samples'):
            current = batch_idx * self.train_loader.batch_size
            total = self.train_loader.n_samples
        else:
            current = batch_idx
            total = self.len_epoch
        return base.format(current, total, 100.0 * current / total)




