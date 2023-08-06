# -*- coding: utf-8 -*-
# @Time    : 2021/10/6 12:25 下午
# @Author  : jeffery
# @FileName: vocabulary.py
# @website : http://www.jeffery.ink/
# @github  : https://github.com/jeffery0628
# @Description:

from typing import *
import my_tools_package.nlp.constants as constants


class TermIndex(dict):
    """Map term to index"""

    def __missing__(self, key):
        """Map out-of-vocabulary terms to index 1."""
        return 1


class Vocabulary:
    def __init__(self, pad_value: str = constants.PAD_WORD, oov_value: str = constants.UNK_WORD):
        self._pad = pad_value
        self._oov = oov_value
        self._context = {
            "term_index": TermIndex(),
            "index_term": dict()
        }
        # 先将Pad和OOV添加到词表中
        self._context['term_index'][self._pad] = 0
        self._context['term_index'][self._oov] = 1
        self._context['index_term'][0] = self._pad
        self._context['index_term'][1] = self._oov

    def fit(self, tokens: Union[List[str], Set[str]]) -> None:
        for term in tokens:
            if term not in self._context["term_index"]:
                self._context["term_index"].setdefault(term, len(self._context["term_index"]))
                self._context["index_term"].setdefault(len(self._context["index_term"]), term)

    def transform(self, input_: list) -> Union[List[int], List[List[int]], None]:
        """Transform a list of tokens to corresponding indices"""
        try:
            if type(input_[0]) == list:
                return [[self._context['term_index'][token] for token in uttr] for uttr in input_]
            else:
                return [self._context['term_index'][token] for token in input_]
        except Exception as e:
            print(input_)
            raise ValueError(e)

    @property
    def vocab_size(self) -> int:
        return len(self._context["term_index"])

    @property
    def term_index(self) -> Dict[str, int]:
        return self._context["term_index"]

    @property
    def index_term(self) -> Dict[int, str]:
        return self._context["index_term"]

    def __str__(self):
        return f"term_index:\n{str(self._context['term_index'])}\nindex_term:\n{str(self._context['index_term'])}"


if __name__ == '__main__':
    import jieba

    vocab = Vocabulary()

    for s in ["Glove是一种矩阵分解式词向量预训练模型，如果我们要得到目标词w的预训练Embedding目标词w的Embedding表示取决于同语境中的词c的共现关系",
              "因此引入矩阵分解的共现矩阵M，下面先给出共现矩阵M定义",
              "gensim加载glove训练的词向量，glove和word2vec得到词向量文件区别在于word2vec包含向量的数量及其维度"]:
        tokens = jieba.lcut(s)
        vocab.fit(tokens)
    print(vocab)
    print(vocab.vocab_size)
