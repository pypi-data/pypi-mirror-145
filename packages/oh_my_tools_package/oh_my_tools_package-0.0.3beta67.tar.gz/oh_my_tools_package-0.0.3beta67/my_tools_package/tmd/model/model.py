# -*- coding: utf-8 -*-
# @Time    : 2022/4/4 10:30 下午
# @Author  : jeffery
# @FileName: model.py
# @github  : https://github.com/jeffery0628
# @Description:
import os
import torch
from torch import nn
import torch.nn.functional as F
from transformers import AutoModel, AutoConfig
from my_tools_package.tmd.base import BaseModel
from my_tools_package.utils.torch import CRF
from my_tools_package.tmd.layers import SinusoidalPositionEmbedding


# #################################################### NER ####################################################

class TFSNER(BaseModel):

    def __init__(self, tfs, dropout, class_num, is_train=True):
        super(TFSNER, self).__init__()
        self.base_model = tfs.model

        # 是否对bert进行训练
        for name, param in self.base_model.named_parameters():
            param.requires_grad = is_train

        self.dropout = nn.Dropout(dropout)
        self.fc = nn.Linear(tfs.config.hidden_size, class_num)

    def forward(self, inputs):
        base_output = self.base_model(inputs['input_ids'], attention_mask=inputs['attention_masks'])
        seq_out = self.fc(self.dropout(base_output[0]))[:, 1:-1, :]
        outputs = {
            "seq_preds": seq_out
        }
        return outputs


class TFSGPNER(TFSNER):
    """
    全局指针模块
    将序列的每个(start, end)作为整体来进行判断
    """

    def __init__(self, tfs, dropout, heads, head_size, class_num, RoPE=True, is_train=True):
        super(TFSGPNER, self).__init__(tfs, dropout, class_num, is_train)
        self.heads = heads
        self.head_size = head_size
        self.RoPE = RoPE
        self.dense = nn.Linear(tfs.config.hidden_size, self.head_size * self.heads * 2)

    def sequence_masking(self, x, mask, value='-inf', axis=None):
        if mask is None:
            return x
        else:
            if value == '-inf':
                value = -1e12
            elif value == 'inf':
                value = 1e12
            assert axis > 0, 'axis must be greater than 0'
            for _ in range(axis - 1):
                mask = torch.unsqueeze(mask, 1)
            for _ in range(x.ndim - mask.ndim):
                mask = torch.unsqueeze(mask, mask.ndim)
            return x * mask + value * (1 - mask)

    def add_mask_tril(self, logits, mask):
        if mask.dtype != logits.dtype:
            mask = mask.type(logits.dtype)
        logits = self.sequence_masking(logits, mask, '-inf', logits.ndim - 2)
        logits = self.sequence_masking(logits, mask, '-inf', logits.ndim - 1)
        # 排除下三角
        mask = torch.tril(torch.ones_like(logits), diagonal=-1)
        logits = logits - mask * 1e12
        return logits

    def forward(self, inputs):
        base_output = self.base_model(inputs['input_ids'], attention_mask=inputs['attention_masks'])
        seq_out = self.fc(self.dropout(base_output[0]))[:, 1:-1, :]
        mask = inputs['attention_masks'][:, 1:-1, :]

        inputs = self.dense(seq_out)
        inputs = torch.split(inputs, self.head_size * 2, dim=-1)
        # 按照-1这个维度去分，每块包含x个小块
        inputs = torch.stack(inputs, dim=-2)
        # 沿着一个新维度对输入张量序列进行连接。 序列中所有的张量都应该为相同形状
        qw, kw = inputs[..., :self.head_size], inputs[..., self.head_size:]
        # 分出qw和kw
        # RoPE编码
        if self.RoPE:
            pos = SinusoidalPositionEmbedding(self.head_size, 'zero')(inputs)
            cos_pos = pos[..., None, 1::2].repeat(1, 1, 1, 2)
            sin_pos = pos[..., None, ::2].repeat(1, 1, 1, 2)
            qw2 = torch.stack([-qw[..., 1::2], qw[..., ::2]], 4)
            qw2 = torch.reshape(qw2, qw.shape)
            qw = qw * cos_pos + qw2 * sin_pos
            kw2 = torch.stack([-kw[..., 1::2], kw[..., ::2]], 4)
            kw2 = torch.reshape(kw2, kw.shape)
            kw = kw * cos_pos + kw2 * sin_pos
        # 计算内积
        logits = torch.einsum('bmhd , bnhd -> bhmn', qw, kw)
        # 排除padding 排除下三角
        logits = self.add_mask_tril(logits, mask)

        # scale返回
        return logits / self.head_size ** 0.5


class TFSEfficientGPNER(TFSGPNER):
    """
    全局指针模块
    将序列的每个(start, end)作为整体来进行判断
    """

    def __init__(self, tfs, dropout, heads, head_size, class_num, RoPE=True, is_train=True):
        super(TFSEfficientGPNER, self).__init__(tfs, dropout, heads, head_size, class_num, RoPE, is_train)
        self.dense_1 = nn.Linear(tfs.config.hidden_size, self.head_size * 2)
        self.dense_2 = nn.Linear(self.head_size * 2, self.heads * 2)

    def forward(self, inputs):
        base_output = self.base_model(inputs['input_ids'], attention_mask=inputs['attention_masks'])
        seq_out = self.fc(self.dropout(base_output[0]))[:, 1:-1, :]
        mask = inputs['attention_masks'][:, 1:-1, :]

        inputs = self.dense_1(base_output)  # batch,
        # 沿着一个新维度对输入张量序列进行连接。 序列中所有的张量都应该为相同形状
        qw, kw = inputs[..., :self.head_size], inputs[..., self.head_size:]
        # 分出qw和kw
        # RoPE编码
        if self.RoPE:
            pos = SinusoidalPositionEmbedding(self.head_size, 'zero')(inputs)
            cos_pos = pos[..., 1::2].repeat(1, 1, 2)
            sin_pos = pos[..., ::2].repeat(1, 1, 2)
            qw2 = torch.stack([-qw[..., 1::2], qw[..., ::2]], 3)
            qw2 = torch.reshape(qw2, qw.shape)
            qw = qw * cos_pos + qw2 * sin_pos
            kw2 = torch.stack([-kw[..., 1::2], kw[..., ::2]], 3)
            kw2 = torch.reshape(kw2, kw.shape)
            kw = kw * cos_pos + kw2 * sin_pos
        # 计算内积
        logits = torch.einsum('bmd , bnd -> bmn', qw, kw) / self.head_size ** 0.5
        bias = torch.einsum('bnh -> bhn', self.dense_2(inputs)) / 2
        logits = logits[:, None] + bias[:, :self.heads, None] + bias[:, self.heads:, :, None]

        # 排除padding 排除下三角
        logits = self.add_mask_tril(logits, mask)

        # scale返回
        return logits


class PoolerStartLogits(nn.Module):
    def __init__(self, hidden_size, num_classes):
        super(PoolerStartLogits, self).__init__()
        self.dense = nn.Linear(hidden_size, num_classes)

    def forward(self, hidden_states, p_mask=None):
        x = self.dense(hidden_states)
        return x


class PoolerEndLogits(nn.Module):
    def __init__(self, hidden_size, num_classes):
        super(PoolerEndLogits, self).__init__()
        self.dense_0 = nn.Linear(hidden_size, hidden_size)
        self.activation = nn.Tanh()
        self.LayerNorm = nn.LayerNorm(hidden_size)
        self.dense_1 = nn.Linear(hidden_size, num_classes)

    def forward(self, hidden_states, start_positions=None, p_mask=None):
        x = self.dense_0(torch.cat([hidden_states, start_positions], dim=-1))
        x = self.activation(x)
        x = self.LayerNorm(x)
        x = self.dense_1(x)
        return x


class TFSSpanNER(TFSNER):

    def __init__(self, tfs, dropout, class_num, soft_label, is_train=True):
        super(TFSSpanNER, self).__init__(tfs, dropout, is_train, class_num)
        self.num_labels = class_num
        self.soft_label = soft_label
        self.start_fc = PoolerStartLogits(tfs.config.hidden_size, self.num_labels)

        if self.soft_label:
            self.end_fc = PoolerEndLogits(tfs.config.hidden_size + self.num_labels, self.num_labels)
        else:
            self.end_fc = PoolerEndLogits(tfs.config.hidden_size + 1, self.num_labels)

    def forward(self, inputs, training=True):

        base_out = self.base_model(inputs['input_ids'], attention_mask=inputs['attention_masks'])
        sequence_output = self.dropout(base_out[0])

        start_logits = self.start_fc(sequence_output)
        if inputs['start_ids'] is not None and training:
            start_positions_zeros = torch.zeros_like(inputs['start_ids'])
            start_positions_ = torch.where(inputs['start_ids'] > 0, inputs['start_ids'], start_positions_zeros)
            if self.soft_label:
                batch_size = inputs['input_ids'].size(0)
                seq_len = inputs['input_ids'].size(1)
                label_logits = torch.FloatTensor(batch_size, seq_len, self.num_labels)
                label_logits.zero_()
                label_logits = label_logits.to(inputs['input_ids'].device)
                label_logits.scatter_(2, start_positions_.unsqueeze(2), 1)
            else:
                label_logits = start_positions_.unsqueeze(2).float()
        else:
            label_logits = F.softmax(start_logits, -1)
            if not self.soft_label:
                label_logits = torch.argmax(label_logits, -1).unsqueeze(2).float()

        end_logits = self.end_fc(sequence_output, label_logits)

        outputs = {
            'start_logits': start_logits,
            'end_logits': end_logits
        }
        return outputs


class TFSRNNSpanNER(TFSSpanNER):
    def __init__(self, tfs, dropout, class_num, soft_label, rnn_type, out_cat, hidden_dim, n_layers, bidirectional,
                 batch_first=True, is_train=True):
        super(TFSRNNSpanNER, self).__init__(tfs, dropout, class_num, soft_label, is_train)
        self.rnn_type = rnn_type
        self.out_cat = out_cat

        if rnn_type == 'lstm':
            self.rnn = nn.LSTM(self.transformer_model.config.to_dict()['hidden_size'],
                               hidden_size=hidden_dim,
                               num_layers=n_layers,
                               bidirectional=bidirectional,
                               batch_first=batch_first,
                               dropout=dropout)
        elif rnn_type == 'gru':
            self.rnn = nn.GRU(self.transformer_model.config.to_dict()['hidden_size'],
                              hidden_size=hidden_dim,
                              num_layers=n_layers,
                              bidirectional=bidirectional,
                              batch_first=batch_first,
                              dropout=dropout)
        else:
            self.rnn = nn.RNN(self.transformer_model.config.to_dict()['hidden_size'],
                              hidden_size=hidden_dim,
                              num_layers=n_layers,
                              bidirectional=bidirectional,
                              batch_first=batch_first,
                              dropout=dropout)

        if out_cat:
            if bidirectional:
                self.start_fc = PoolerStartLogits(tfs.config.hidden_size + hidden_dim * 2, self.num_labels)
                if self.soft_label:
                    self.end_fc = PoolerEndLogits(tfs.config.hidden_size + self.num_labels + hidden_dim * 2,
                                                  self.num_labels)
                else:
                    self.end_fc = PoolerEndLogits(tfs.config.hidden_size + 1 + hidden_dim * 2, self.num_labels)
            else:
                self.start_fc = PoolerStartLogits(tfs.config.hidden_size + hidden_dim, self.num_labels)
                if self.soft_label:
                    self.end_fc = PoolerEndLogits(tfs.config.hidden_size + self.num_labels + hidden_dim,
                                                  self.num_labels)
                else:
                    self.end_fc = PoolerEndLogits(tfs.config.hidden_size + 1 + hidden_dim, self.num_labels)
        else:
            if bidirectional:
                self.start_fc = PoolerStartLogits(hidden_dim * 2, self.num_labels)

                if self.soft_label:
                    self.end_fc = PoolerEndLogits(hidden_dim * 2 + self.num_labels, self.num_labels)
                else:
                    self.end_fc = PoolerEndLogits(hidden_dim * 2 + 1, self.num_labels)
            else:

                self.start_fc = PoolerStartLogits(hidden_dim, self.num_labels)

                if self.soft_label:
                    self.end_fc = PoolerEndLogits(hidden_dim + self.num_labels, self.num_labels)
                else:
                    self.end_fc = PoolerEndLogits(hidden_dim + 1, self.num_labels)

    def forward(self, inputs, training=True):
        base_out = self.base_model(inputs['input_ids'], attention_mask=inputs['attention_masks'])
        if self.rnn_type in ['rnn', 'gru']:
            rnn_output, hidden = self.rnn(self.dropout(base_out[0]))
        else:
            rnn_output, (hidden, cell) = self.rnn(self.dropout(base_out[0]))

        if self.out_cat:
            out = torch.cat([base_out[0], rnn_output], dim=-1)
        else:
            out = rnn_output

        sequence_output = self.dropout(out)

        start_logits = self.start_fc(sequence_output)
        if inputs['start_ids'] is not None and training:
            start_positions_zeros = torch.zeros_like(inputs['start_ids'])
            start_positions_ = torch.where(inputs['start_ids'] > 0, inputs['start_ids'], start_positions_zeros)
            if self.soft_label:
                batch_size = inputs['input_ids'].size(0)
                seq_len = inputs['input_ids'].size(1)
                label_logits = torch.FloatTensor(batch_size, seq_len, self.num_labels)
                label_logits.zero_()
                label_logits = label_logits.to(inputs['input_ids'].device)
                label_logits.scatter_(2, start_positions_.unsqueeze(2), 1)
            else:
                label_logits = start_positions_.unsqueeze(2).float()
        else:
            label_logits = F.softmax(start_logits, -1)
            if not self.soft_label:
                label_logits = torch.argmax(label_logits, -1).unsqueeze(2).float()

        end_logits = self.end_fc(sequence_output, label_logits)

        outputs = {
            'start_logits': start_logits,
            'end_logits': end_logits
        }
        return outputs


class TFSMidNER(TFSNER):

    def __init__(self, tfs, dropout, is_train, class_num, output_hidden_layers):
        super(TFSMidNER, self).__init__(tfs, dropout, is_train, class_num)
        self.output_hidden_layers = output_hidden_layers
        self.act_fun = nn.GELU()
        self.middle_fc = nn.Linear(tfs.config['hidden_size'] * len(output_hidden_layers),
                                   tfs.config['hidden_size'])
        self.layer_norm = nn.LayerNorm(tfs.config.to_dict()['hidden_size'])

    def forward(self, inputs):
        base_output = self.base_model(inputs['input_ids'], attention_mask=inputs['attention_masks'])
        hidden_layers = []
        for layer_index in self.output_hidden_layers:
            hidden_layers.append(base_output[2][layer_index - 1])

        middle_out = self.middle_fc(torch.cat(hidden_layers, dim=-1))
        middle_out = self.act_fun(middle_out)
        middle_out = self.layer_norm(middle_out)
        middle_out = self.dropout(middle_out)
        seq_out = self.fc(middle_out)[:, 1:-1, :]
        outputs = {
            "seq_preds": seq_out
        }
        return outputs


class TFSCRFNER(TFSNER):

    def __init__(self, tfs, dropout,  class_num,is_train=True):
        super(TFSCRFNER, self).__init__(tfs=tfs, dropout=dropout,class_num=class_num,is_train=is_train)
        self.crf = CRF(num_tags=class_num, batch_first=True)

    def forward(self, inputs):
        base_output = self.base_model(inputs['input_ids'], attention_mask=inputs['attention_masks'])
        seq_out = self.fc(self.dropout(base_output[0]))[:, 1:-1, :]
        crf_mask = inputs['attention_masks'][:, 1:-1]
        loss = None
        if inputs['labels'] is not None:
            loss = - self.crf(emissions=seq_out, tags=inputs['labels'], mask=crf_mask)
        outputs = {
            "seq_preds": seq_out,
            "loss": loss
        }
        return outputs


class TFSRNNNER(TFSNER):

    def __init__(self, tfs, dropout, class_num, rnn_type, hidden_dim, n_layers, bidirectional,
                 batch_first=True, out_cat=False, is_train=True):
        super(TFSRNNNER, self).__init__(tfs, dropout, is_train, class_num)
        self.rnn_type = rnn_type
        if rnn_type == 'lstm':
            self.rnn = nn.LSTM(self.transformer_model.config.to_dict()['hidden_size'],
                               hidden_size=hidden_dim,
                               num_layers=n_layers,
                               bidirectional=bidirectional,
                               batch_first=batch_first,
                               dropout=dropout)
        elif rnn_type == 'gru':
            self.rnn = nn.GRU(self.transformer_model.config.to_dict()['hidden_size'],
                              hidden_size=hidden_dim,
                              num_layers=n_layers,
                              bidirectional=bidirectional,
                              batch_first=batch_first,
                              dropout=dropout)
        else:
            self.rnn = nn.RNN(self.transformer_model.config.to_dict()['hidden_size'],
                              hidden_size=hidden_dim,
                              num_layers=n_layers,
                              bidirectional=bidirectional,
                              batch_first=batch_first,
                              dropout=dropout)

        self.out_cat = out_cat
        if out_cat:
            if bidirectional:
                self.fc = nn.Linear(self.transformer_model.config.to_dict()['hidden_size'] + hidden_dim * 2, class_num)
            else:
                self.fc = nn.Linear(self.transformer_model.config.to_dict()['hidden_size'] + hidden_dim, class_num)
        else:
            if bidirectional:
                self.fc = nn.Linear(hidden_dim * 2, class_num)
            else:
                self.fc = nn.Linear(hidden_dim, class_num)

    def forward(self, inputs):
        base_out = self.base_model(inputs['input_ids'], attention_mask=inputs['attention_masks'])

        if self.rnn_type in ['rnn', 'gru']:
            rnn_output, hidden = self.rnn(self.dropout(base_out[0]))
        else:
            rnn_output, (hidden, cell) = self.rnn(self.dropout(base_out[0]))
        if self.out_cat:
            out = torch.cat([base_out[0], rnn_output], dim=-1)
        else:
            out = rnn_output
        seq_out = self.fc(self.dropout(out))[:, 1:-1, :]
        outputs = {
            "seq_preds": seq_out
        }
        return outputs


class TFSRNNCRFNER(TFSRNNNER):

    def __init__(self, tfs, dropout, class_num, rnn_type, hidden_dim, n_layers, bidirectional,
                 batch_first=True, out_cat=False, is_train=True):
        super(TFSRNNCRFNER, self).__init__(tfs, dropout, class_num, rnn_type, hidden_dim, n_layers, bidirectional,
                                           batch_first=True, out_cat=False, is_train=True)
        self.crf = CRF(num_tags=class_num, batch_first=True)

    def forward(self, inputs):

        base_output = self.base_model(inputs['input_ids'], attention_mask=inputs['attention_masks'])

        if self.rnn_type in ['rnn', 'gru']:
            rnn_output, hidden = self.rnn(self.dropout(base_output[0]))
        else:
            rnn_output, (hidden, cell) = self.rnn(self.dropout(base_output[0]))

        if self.out_cat:
            out = torch.cat([base_output[0], rnn_output], dim=-1)
        else:
            out = rnn_output

        out = self.fc(self.dropout(out))[:, 1:-1]
        crf_mask = inputs['attention_masks'][:, 1:-1]
        loss = None
        if inputs['labels'] is not None:
            loss = - self.crf(emissions=out, tags=inputs['labels'], mask=crf_mask)

        outputs = {
            "seq_preds": out,
            "loss": loss
        }
        return outputs

# #################################################### NER ####################################################
