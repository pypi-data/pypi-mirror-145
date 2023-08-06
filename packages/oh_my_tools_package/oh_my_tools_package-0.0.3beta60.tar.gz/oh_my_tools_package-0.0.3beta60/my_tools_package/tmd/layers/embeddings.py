# -*- coding: utf-8 -*-
# @Time    : 2022/4/4 11:15 下午
# @Author  : jeffery
# @FileName: embeddings.py
# @github  : https://github.com/jeffery0628
# @Description:
import math

import torch
import torch.nn as nn
from torch.nn import Module
from my_tools_package.tmd.layers import LayerNorm


class SinusoidalPositionEmbedding(Module):
    """
    定义Sin-Cos位置Embedding
    """

    def __init__(self, output_dim, merge_mode='add', custom_position_ids=False):
        super(SinusoidalPositionEmbedding, self).__init__()
        self.output_dim = output_dim
        self.merge_mode = merge_mode
        self.custom_position_ids = custom_position_ids

    def forward(self, inputs):
        input_shape = inputs.shape
        _, seq_len = input_shape[0], input_shape[1]
        position_ids = torch.arange(seq_len).type(torch.float)[None]
        indices = torch.arange(self.output_dim // 2).type(torch.float)
        indices = torch.pow(10000.0, -2 * indices / self.output_dim)
        embeddings = torch.einsum('bn,d->bnd', position_ids, indices)
        embeddings = torch.stack([torch.sin(embeddings), torch.cos(embeddings)], dim=-1)
        embeddings = torch.reshape(embeddings, (-1, seq_len, self.output_dim))

        if self.merge_mode == 'add':
            return inputs + embeddings.to(inputs.device)
        elif self.merge_mode == 'mul':
            return inputs * (embeddings + 1.0).to(inputs.device)
        elif self.merge_mode == 'zero':
            return embeddings.to(inputs.device)


class WordEmbedding(nn.Module):
    """
    """

    def __init__(self, dropout, vocab_size, emb_size, remove_embedding_layernorm=False):
        super(WordEmbedding, self).__init__()
        self.remove_embedding_layernorm = remove_embedding_layernorm
        self.dropout = nn.Dropout(dropout)
        self.word_embedding = nn.Embedding(vocab_size, emb_size)
        if not self.remove_embedding_layernorm:
            self.layer_norm = LayerNorm(emb_size)

    def forward(self, src, _):
        """
        Args:
            src: [batch_size x seq_length]
            seg: [batch_size x seq_length]
        Returns:
            emb: [batch_size x seq_length x hidden_size]
        """
        emb = self.word_embedding(src)
        if not self.remove_embedding_layernorm:
            emb = self.layer_norm(emb)
        emb = self.dropout(emb)
        return emb


class WordPosEmbedding(WordEmbedding):
    """
    GPT embedding consists of two parts:
    word embedding and position embedding.
    """

    def __init__(self, dropout, vocab_size, emb_size, max_seq_length, remove_embedding_layernorm=False):
        super(WordPosEmbedding, self).__init__(dropout, vocab_size, emb_size, remove_embedding_layernorm)
        self.max_seq_length = max_seq_length
        self.position_embedding = nn.Embedding(self.max_seq_length, emb_size)

    def forward(self, src, _):
        """
        Args:
            src: [batch_size x seq_length]
            seg: [batch_size x seq_length]
        Returns:
            emb: [batch_size x seq_length x hidden_size]
        """
        word_emb = self.word_embedding(src)
        pos_emb = self.position_embedding(
            torch.arange(0, word_emb.size(1), device=word_emb.device, dtype=torch.long)
                .unsqueeze(0)
                .repeat(word_emb.size(0), 1)
        )

        emb = word_emb + pos_emb
        if not self.remove_embedding_layernorm:
            emb = self.layer_norm(emb)
        emb = self.dropout(emb)
        return emb


class WordPosSegEmbedding(WordPosEmbedding):
    """
    BERT embedding consists of three parts:
    word embedding, position embedding, and segment embedding.
    """

    def __init__(self, dropout, vocab_size, emb_size, max_seq_length, remove_embedding_layernorm=False):
        super(WordPosSegEmbedding, self).__init__(dropout, vocab_size, emb_size, max_seq_length,
                                                  remove_embedding_layernorm)
        self.segment_embedding = nn.Embedding(3, emb_size)

    def forward(self, src, seg):
        """
        Args:
            src: [batch_size x seq_length]
            seg: [batch_size x seq_length]
        Returns:
            emb: [batch_size x seq_length x hidden_size]
        """
        word_emb = self.word_embedding(src)
        pos_emb = self.position_embedding(
            torch.arange(0, word_emb.size(1), device=word_emb.device, dtype=torch.long)
                .unsqueeze(0)
                .repeat(word_emb.size(0), 1)
        )
        seg_emb = self.segment_embedding(seg)

        emb = word_emb + pos_emb + seg_emb
        if not self.remove_embedding_layernorm:
            emb = self.layer_norm(emb)
        emb = self.dropout(emb)
        return emb



class RelativePositionEmbedding(nn.Module):
    """ Relative Position Embedding
        https://arxiv.org/abs/1910.10683
        https://github.com/bojone/bert4keras/blob/db236eac110a67a587df7660f6a1337d5b2ef07e/bert4keras/layers.py#L663
        https://github.com/huggingface/transformers/blob/master/src/transformers/models/t5/modeling_t5.py#L344
    """

    def __init__(self, heads_num, bidirectional=True, num_buckets=32, max_distance=128):
        super(RelativePositionEmbedding, self).__init__()
        self.num_buckets = num_buckets
        self.bidirectional = bidirectional
        self.max_distance = max_distance
        self.relative_attention_bias = nn.Embedding(self.num_buckets, heads_num)

    def forward(self, encoder_hidden, decoder_hidden):
        """
        Compute binned relative position bias
        Args:
            encoder_hidden: [batch_size x seq_length x emb_size]
            decoder_hidden: [batch_size x seq_length x emb_size]
        Returns:
            position_bias: [1 x heads_num x seq_length x seq_length]
        """
        query_length = encoder_hidden.size()[1]
        key_length = decoder_hidden.size()[1]

        context_position = torch.arange(query_length, dtype=torch.long)[:, None]
        memory_position = torch.arange(key_length, dtype=torch.long)[None, :]
        relative_position = memory_position - context_position  # shape (query_length, key_length)
        relative_position_bucket = self.relative_position_bucket(
            relative_position,  # shape (query_length, key_length)
            bidirectional=self.bidirectional,
            num_buckets=self.num_buckets,
            max_distance=self.max_distance
        )
        relative_position_bucket = relative_position_bucket.to(self.relative_attention_bias.weight.device)
        values = self.relative_attention_bias(relative_position_bucket)  # shape (query_length, key_length, num_heads)
        values = values.permute([2, 0, 1]).unsqueeze(0)  # shape (1, num_heads, query_length, key_length)
        return values

    def relative_position_bucket(self, relative_position, bidirectional, num_buckets, max_distance):
        """
        Adapted from Mesh Tensorflow:
        https://github.com/tensorflow/mesh/blob/0cb87fe07da627bf0b7e60475d59f95ed6b5be3d/mesh_tensorflow/transformer/transformer_layers.py#L593
        Translate relative position to a bucket number for relative attention. The relative position is defined as
        memory_position - query_position, i.e. the distance in tokens from the attending position to the attended-to
        position. If bidirectional=False, then positive relative positions are invalid. We use smaller buckets for
        small absolute relative_position and larger buckets for larger absolute relative_positions. All relative
        positions >=max_distance map to the same bucket. All relative positions <=-max_distance map to the same bucket.
        This should allow for more graceful generalization to longer sequences than the model has been trained on
        Args:
            relative_position: an int32 Tensor
            bidirectional: a boolean - whether the attention is bidirectional
            num_buckets: an integer
            max_distance: an integer
        Returns:
            a Tensor with the same shape as relative_position, containing int32 values in the range [0, num_buckets)
        """
        relative_buckets = 0
        if bidirectional:
            num_buckets //= 2
            relative_buckets += (relative_position > 0).to(torch.long) * num_buckets
            relative_position = torch.abs(relative_position)
        else:
            relative_position = -torch.min(relative_position, torch.zeros_like(relative_position))
        # now relative_position is in the range [0, inf)

        # half of the buckets are for exact increments in positions
        max_exact = num_buckets // 2
        is_small = relative_position < max_exact

        # The other half of the buckets are for logarithmically bigger bins in positions up to max_distance
        relative_postion_if_large = max_exact + (
                torch.log(relative_position.float() / max_exact)
                / math.log(max_distance / max_exact)
                * (num_buckets - max_exact)
        ).to(torch.long)
        relative_postion_if_large = torch.min(
            relative_postion_if_large, torch.full_like(relative_postion_if_large, num_buckets - 1)
        )

        relative_buckets += torch.where(is_small, relative_position, relative_postion_if_large)
        return relative_buckets