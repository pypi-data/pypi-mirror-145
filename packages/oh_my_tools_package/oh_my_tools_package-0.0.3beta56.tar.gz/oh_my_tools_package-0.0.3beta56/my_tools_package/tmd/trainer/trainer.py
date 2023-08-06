# -*- coding: utf-8 -*-
# @Time    : 2022/4/4 10:12 下午
# @Author  : jeffery
# @FileName: trainer.py
# @github  : https://github.com/jeffery0628
# @Description:
import json

import numpy as np
import pandas as pd
import torch

from my_tools_package.tmd.base import BaseTrainer
from my_tools_package.tmd.metric import MetricTracker
from my_tools_package.utils.torch import NERUtils


class CRFTrainer(BaseTrainer):
    """
    Trainer class
    """

    def __init__(self, i_fold, device, device_ids, model, optimizer, criterions, metric_ftns, logger, tmd_config,
                 id2label, train_loader, valid_loader=None, test_loader=None, lr_scheduler=None,
                 len_epoch=None):
        super().__init__(i_fold=i_fold, device=device, device_ids=device_ids, model=model, optimizer=optimizer,
                         criterions=criterions, metric_ftns=metric_ftns, logger=logger, tmd_config=tmd_config)
        self.id2label = id2label
        self.train_loader = train_loader
        self.i_fold = i_fold
        if len_epoch is None:
            self.len_epoch = len(self.train_loader)
        else:
            # iteration-based training
            self.train_loader = self.inf_loop(train_loader)
            self.len_epoch = len_epoch
        self.valid_loader = valid_loader
        self.test_loader = test_loader
        self.do_validation = self.valid_loader is not None
        self.do_inference = self.test_loader is not None
        self.lr_scheduler = lr_scheduler
        self.log_step = int(np.sqrt(train_loader.batch_size))

        self.train_metrics = MetricTracker('loss', *[m.__name__ for m in self.metric_ftns], writer=self.writer)
        self.valid_metrics = MetricTracker('loss', *[m.__name__ for m in self.metric_ftns], writer=self.writer)

    def _train_epoch(self, epoch):
        """
        Training logic for an epoch
        """
        self.model.zero_grad()
        self.train_metrics.reset()
        self.model.train()
        for batch_idx, data in enumerate(self.train_loader):
            inputs = {
                'input_ids': data['input_ids'].to(self.device),
                'attention_masks': data['attention_masks'].to(self.device),
                'labels': data['label_ids'].to(self.device)
            }

            outputs = self.model(inputs)
            loss = outputs['loss']
            if len(self.device_ids) > 1:
                loss = outputs['loss'].mean()

            # 损失截断
            loss_zeros = torch.zeros_like(loss)
            loss = torch.where(loss > float(self.tmd_config.tricks.loss_trick.loss_cut), loss, loss_zeros)
            loss.backward()

            if self.tmd_config.tricks.grad_trick.clip_grad:  # 梯度截断
                torch.nn.utils.clip_grad_norm_(self.model.parameters(),
                                               self.tmd_config.tricks.grad_trick.max_grad_norm)

            self.optimizer.step()
            if self.lr_scheduler is not None:
                self.lr_scheduler.step()
            self.model.zero_grad()
            self.writer.set_step((epoch - 1) * self.len_epoch + batch_idx)
            self.train_metrics.update('loss', loss.item())

            if len(self.device_ids) > 1:
                preds = self.model.module.crf.decode(emissions=outputs['seq_preds'],
                                                     mask=inputs['attention_masks'][:, 1:-1])
            else:
                preds = self.model.crf.decode(emissions=outputs['seq_preds'], mask=inputs['attention_masks'][:, 1:-1])

            preds = preds.squeeze(0).cpu().detach().numpy()
            labels = data['label_ids'].numpy()
            preds_entities = [[ent[0], ent[1], ent[2], text[ent[0]:ent[1]]] for pred_entities, text in
                              zip(NERUtils.get_entities_batch(preds, data['text_lengths'], self.id2label), data['text'])
                              for ent
                              in pred_entities]
            labels_entities = [[ent[0], ent[1], ent[2], text[ent[0]:ent[1]]] for label_entities, text in
                               zip(NERUtils.get_entities_batch(labels, data['text_lengths'], self.id2label),
                                   data['text']) for
                               ent in label_entities]
            pred_entities = [p_e for p_e in preds_entities]
            label_entities = [l_e for l_e in labels_entities]
            # 评测
            for met in self.metric_ftns:
                self.train_metrics.update(met.__name__, met(label_entities, pred_entities), n=len(labels))

            if batch_idx % self.log_step == 0:
                self.logger.debug('Train Epoch: {} {} Loss: {:.4f} lr: {}'.format(epoch, self._progress(batch_idx),
                                                                                  loss.item(),
                                                                                  round(self.optimizer.param_groups[0]['lr'],4)))

            if batch_idx == self.len_epoch:
                break

        log = self.train_metrics.result()

        if self.do_validation:
            val_log = self._valid_epoch(epoch)
            log.update(**{'val_' + k: v for k, v in val_log.items()})
        return log

    def _valid_epoch(self, epoch):
        """
        Validate after training an epoch

        :param epoch: Integer, current training epoch.
        :return: A log that contains information about validation
        """
        self.model.eval()
        self.valid_metrics.reset()

        with torch.no_grad():
            for batch_idx, data in enumerate(self.valid_loader):
                inputs = {
                    'input_ids': data['input_ids'].to(self.device),
                    'attention_masks': data['attention_masks'].to(self.device),
                    'labels': data['label_ids'].to(self.device)
                }

                outputs = self.model(inputs)
                loss = outputs['loss']
                if len(self.device_ids) > 1:
                    loss = outputs['loss'].mean()

                if self.add_graph:
                    input_model = self.model.module if (len(self.device_ids) > 1) else self.model
                    self.writer.writer.add_graph(input_model, [inputs])
                    self.add_graph = False

                self.writer.set_step((epoch - 1) * len(self.valid_loader) + batch_idx, 'valid')
                self.valid_metrics.update('loss', loss.item())
                # 多卡
                if len(self.device_ids) > 1:
                    preds = self.model.module.crf.decode(emissions=outputs['seq_preds'],
                                                         mask=inputs['attention_masks'][:, 1:-1])
                else:
                    preds = self.model.crf.decode(emissions=outputs['seq_preds'],
                                                  mask=inputs['attention_masks'][:, 1:-1])
                # 最大路径
                preds = preds.squeeze(0).cpu().detach().numpy()
                labels = data['label_ids'].numpy()

                # 评测
                preds_entities = [(idx, text, [ent[0], ent[1], ent[2], text[ent[0]:ent[1]]]) for
                                  pred_entities, text, idx in
                                  zip(NERUtils.get_entities_batch(preds, data['text_lengths'], self.id2label),
                                      data['text'], data["ids"]) for ent in pred_entities]
                labels_entities = [(idx, text, [ent[0], ent[1], ent[2], text[ent[0]:ent[1]]]) for
                                   label_entities, text, idx in
                                   zip(NERUtils.get_entities_batch(labels, data['text_lengths'], self.id2label),
                                       data['text'], data["ids"]) for ent in label_entities]
                pred_entities = [p_e[2] for p_e in preds_entities]
                label_entities = [l_e[2] for l_e in labels_entities]

                self.diff_track(preds_entities, labels_entities)
                for met in self.metric_ftns:
                    self.valid_metrics.update(met.__name__, met(label_entities, pred_entities), n=len(labels))

        log = self.valid_metrics.result()
        self.save_diff(log)
        # add histogram of model parameters to the tensorboard
        for name, p in self.model.named_parameters():
            self.writer.add_histogram(name, p, bins='auto')
        return log

    def _inference(self):
        """
        Inference after training an epoch
        """
        if self.tmd_config.trainer.resume_path:
            self._resume_checkpoint(self.tmd_config.trainer.resume_path)

        result_path = self.result_dir / f"epoch-{self.i_fold}_{self.mnt_best}.txt"
        result_writer = result_path.open('w', encoding="utf8")
        # inference
        with torch.no_grad():
            for batch_idx, data in enumerate(self.test_loader):
                inputs = {
                    'input_ids': data['input_ids'].to(self.device),
                    'attention_masks': data['attention_masks'].to(self.device),
                    'labels': data['label_ids'].to(self.device)
                }
                outputs = self.model(inputs)
                if len(self.device_ids) > 1:
                    preds = self.model.module.crf.decode(emissions=outputs['seq_preds'],
                                                         mask=inputs['attention_masks'][:, 1:-1])
                else:
                    preds = self.model.crf.decode(emissions=outputs['seq_preds'],
                                                  mask=inputs['attention_masks'][:, 1:-1])
                preds = preds.squeeze(0).cpu().detach().numpy()

                for pred_ids, item_id, text, length in zip(preds, data['ids'], data['text'], data['text_lengths']):
                    pred_entities = NERUtils.get_entities(pred_ids[:length], self.id2label)
                    lbs = [[ent[0], ent[1], ent[2], text[ent[0]:ent[1]]] for ent in pred_entities]
                    result_writer.write(json.dumps({
                        "id": item_id,
                        "text": text,
                        "labels": lbs
                    }, ensure_ascii=False) + '\n')
        result_writer.close()
        self.logger.info(f'result saving to {str(result_path)}')

    def diff_track(self, batch_pred, batch_label):

        for idx, text, pred in batch_pred:
            if idx not in self.valid_diff:
                self.valid_diff[idx] = {
                    "text": text,
                    "preds": [pred],
                    "labels": []
                }
            else:
                self.valid_diff[idx]["preds"].append(pred)
        for idx, text, label in batch_label:
            if idx not in self.valid_diff:
                self.valid_diff[idx] = {
                    "text":text,
                    "preds":[],
                    "labels":[label]
                }
            else:
                self.valid_diff[idx]["labels"].append(label)

    def save_diff(self,log):
        diff_path = self.diff_dir / f"epoch-{self.i_fold}_{round(log['entity_f1'],2)}.csv"
        datas = []
        for idx,v in self.valid_diff.items():
            datas.append({
                "idx":idx,
                "text":v["text"],
                "preds":v["preds"],
                "labels":v["labels"]
            })
        diff_pd = pd.DataFrame(datas)

        diff_pd.to_csv(diff_path, index=False)
        self.logger.info(f"diff file saved to {diff_path}")
        self.valid_diff = {}
