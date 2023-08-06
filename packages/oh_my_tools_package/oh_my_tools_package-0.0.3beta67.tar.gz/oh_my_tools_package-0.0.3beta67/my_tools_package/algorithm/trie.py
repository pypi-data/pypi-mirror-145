# -*- coding: utf-8 -*-
# @Time    : 2021/8/23 8:44 上午
# @Author  : jeffery
# @FileName: trie.py
# @website : http://www.jeffery.ink/
# @github  : https://github.com/jeffery0628
# @Description:

import collections
from typing import *
from pathlib import Path
from abc import abstractmethod, ABCMeta


class TrieNode:
    """
    字典树中的节点
    """

    def __init__(self):
        """
            children:表示子节点
            is_leaf: 是否为词结束的标志
            insert_freq: 插入频次
            search_freq: 搜索频次
        """
        self.children = collections.defaultdict(TrieNode)
        self.is_leaf = False
        self.insert_freq = 0
        self.search_freq = 0


class CharTrie:
    """
    字符字典树，比较适合词级别的查找，字典树中每个节点的键对应着一个字符
    """

    def __init__(self):
        self.root = TrieNode()

    @classmethod
    def from_words(cls, words: List[str], min_len: int = 0):
        """

        Args:
            words: 列表类型的词典：[word1,word2,word3,...]
            min_len  : 词的最小长度,包含最小长度
        Returns:
            返回以词表构建的字典树
        """
        trie = cls()
        for word in words:
            if not len(word) >= min_len:
                continue
            trie.insert(word)
        return trie

    @classmethod
    def from_file(cls, word_file: Union[str, Path], min_len: int = 0, encoding="utf8"):
        """

        Args:
            word_file: 词表文件，文件内容格式，每行一个词：
                        word1,
                        word2,
                        word3,
                        ...
            min_len  : 词的最小长度,包含最小长度

        Returns:
            返回以词表构建的字典树
        """
        trie = cls()
        word_file = Path(word_file)
        with word_file.open("r", encoding=encoding) as f:
            for word in f:
                word = word.strip()
                if not len(word) >= min_len:
                    continue
                trie.insert(word)
        return trie

    def insert(self, word: str):
        """
        Args:
            word: 向字典树中插入的词
        Returns:
        """
        current = self.root
        for char in word:
            current = current.children[char]
        current.is_leaf = True
        current.insert_freq += 1

    def search_word_with_freq(self, word: str) -> List[int]:
        """
        查询word，如果word在字典树中存在，返回word的插入频次和搜索频次
        Args:
            word: 被查询的词

        Returns:
            [-1,0,0]
            [0,0,0]
            [1,insert_freq,search_freq]

        """
        current = self.root
        for char in word:
            current = current.children.get(char)
            if current is None:
                return [-1, 0, 0]
        if current.is_leaf:
            current.search_freq += 1
            return [1, current.insert_freq, current.search_freq]

        return [0, 0, 0]

    def search(self, word: str) -> int:
        """

        Args:
            word:在字典树中搜索word

        Returns:
            -1: 词不存在于字典中
            0 : 该词在字典中是一个前缀
            1 : 该词存在于字典中
        """

        current = self.root
        for char in word:
            current = current.children.get(char)
            if current is None:
                return -1
        if current.is_leaf:
            current.search_freq += 1
            return 1

        return 0

    def contain(self, word: str) -> bool:
        """

        Args:
            word:判读字典树是否包含word

        Returns:
            如果包含返回True，否则 False
        """

        current = self.root
        for char in word:
            current = current.children.get(char, None)
            if current is None:
                return False
        if current.is_leaf:
            current.search_freq += 1
            return True
        return False

    def clear(self):
        self.root = TrieNode()

    def delete(self, word: str) -> int:
        """

        Args:
            word: 在字典树中搜索word,如果word存在，删除word

        Returns:
            -1 : 词不存在于字典中
            0  : 该词在字典中是一个前缀
            1 : 从字典中删除该词
        """
        current = self.root
        for char in word:
            current = current.children.get(char)
            if current is None:
                return -1
        if current.is_leaf:
            current.is_leaf = False
            current.search_freq = 0
            current.insert_freq = 0
            return 1
        return 0

    def start_with(self, prefix: str):
        """
        搜索以prefix为前缀的所有词
        Args:
            prefix: 前缀词

        Returns:
            返回列表，列表中包含：字典树中所有以prefix作为前缀的词
        """

        result = []
        chars = []
        current = self.root
        for char in prefix:
            chars.append(char)
            current = current.children.get(char)
            if current is None:
                return result

        self._dfs_prefix_word(current, chars, result)
        return result

    def get_words(self) -> List[str]:
        """

        Returns:
            返回字典树中所有的词
        """
        words = []
        self._dfs_prefix_word(node=self.root, chars=[], result=words)
        return words

    def _dfs_prefix_word(self, node: TrieNode, chars: List[str], result: List[str]):
        if node.is_leaf:
            result.append("".join(chars))

        for key, value in node.children.items():
            chars.append(key)
            self._dfs_prefix_word(value, chars, result)
            chars.pop()

    def get_lexicon(self, sentence: str):
        """
        查找sentence中的所有词
        Args:
            sentence: 句子

        Returns: [[start1,end1,word1],[start2,end2,word2],...]
            返回句子在词典中所包含的所有的词汇
        """
        result = []
        for i in range(len(sentence)):
            current = self.root
            for j in range(i, len(sentence)):
                current = current.children.get(sentence[j])
                if current is None:
                    break
                if current.is_leaf:
                    result.append([i, j + 1, sentence[i:j + 1], current.freq])
        return result

    def merge_trie(self, other_trie):
        for word in other_trie.get_words():
            self.insert(word)


class StringTrie:
    """
    字符串字典树，比较适合句子级别的查找，字典树中的每个节点对应一个词
    """

    def __init__(self):
        self.root = TrieNode()

    @classmethod
    def from_sentences(cls, sentences: Union[List[str], Set[str], List[List[str]]], sep: str = "/"):
        """
        Args:
            sentences: 包含已经分词的多个句子的集合
                        数据格式：①["word1/word2/word3","word4/word5/word6",...]
                                ②{"word1/word2/word3","word4/word5/word6",...}
                                ③[[word1,word2,word3],[word4,word5,word6],...]
            sep:将句子分成词的分隔符
        Returns:
        """
        trie = StringTrie()
        for sentence in sentences:
            trie.insert(sentence)
        return trie

    @classmethod
    def from_file(cls, file_path: Union[str, Path], sep: str = "/", encoding="utf8"):
        """
        从 文件 构建句子字典树
        Args:
            file_path: 文件路径,文件中数据格式,词的分割方式由sep指定，默认:'/'：
                    word1/word2/word3
                    word4/word5/word6
                or
                    word1 word2 word3
                    word4 word5 word6
                or
                    ...
            sep: 词的分割方式，默认："/"
            encoding: 文件编码格式，默认utf8
        Returns:

        """
        trie = cls()
        file_path = Path(file_path)
        with file_path.open('r', encoding=encoding) as f:
            for line in f:
                trie.insert(line)
        return trie

    def insert(self, sentence: Union[str, List[str]], sep: str = "/") -> None:
        """

        Args:
            sentence:需要向字典树插入的句子，数据格式：[word1,word2,word3]
            sep:将句子分成词的分隔符
        Returns:

        """
        if isinstance(sentence, str):
            sentence = sentence.strip().split(sep)
        current = self.root
        for word in sentence:
            current = current.children.get(word)
        current.is_leaf = True
        current.insert_freq += 1

    def search_sentence_with_freq(self, sentence: Union[str, List[str]], sep: str = "/") -> List[int]:
        """
        查询sentence，如果sentence在字典树中存在，返回sentence的插入频次和搜索频次
        Args:
            sentence: 被查询的句子
            sep:词的分隔符

        Returns:
            [-1,0,0]
            [0,0,0]
            [1,insert_freq,search_freq]

        """
        if isinstance(sentence, str):
            sentence = sentence.strip().split(sep)

        current = self.root
        for word in sentence:
            current = current.children.get(word)
            if current is None:
                return [-1, 0, 0]
        if current.is_leaf:
            current.search_freq += 1
            return [1, current.insert_freq, current.search_freq]
        else:
            return [0, 0, 0]

    def search(self, sentence: Union[str, List[str]], sep: str = "/") -> int:
        """
        查询sentence，如果sentence在字典树中存在，返回sentence的插入频次和搜索频次
        Args:
            sentence: 被查询的句子
            sep:词的分隔符

        Returns:
            -1: 句子不存在于字典中
            0 : 该句子在字典中是一个前缀
            1 : 该句子存在于字典中

        """
        if isinstance(sentence, str):
            sentence = sentence.strip().split(sep)
        current = self.root
        for word in sentence:
            current = current.children.get(word)
            if current is None:
                return -1
        if current.is_leaf:
            current.search_freq += 1
            return 1
        else:
            return 0

    def contain(self, sentence: Union[str, List[str]], sep: str = '/') -> bool:
        if isinstance(sentence, str):
            sentence = sentence.strip().split(sep)
        current = self.root
        for word in sentence:
            current = current.children.get(word)
            if current is None:
                return False
        if current.is_leaf:
            return True
        return False

    def clear(self):
        self.root = TrieNode()

    def delete(self, sentence: Union[str, List[str]], sep: str = "/") -> int:
        """

        Args:
            sentence: 在字典树中搜索sentence,如果sentence存在，删除sentence
            sep: 句子中 词之间的分隔符
        Returns:
            -1 : 句子不存在于字典中
            0  : 该句子在字典中是一个前缀
            1 : 从字典中删除该句子
        """
        if isinstance(sentence, str):
            sentence = sentence.strip().split(sep)

        current = self.root
        for word in sentence:
            current = current.children.get(word)
            if current is None:
                return -1
        if current.is_leaf == True:
            current.is_leaf = False
            current.search_freq = 0
            current.insert_freq = 0
            return 1
        return 0

    def start_with(self, sentence: Union[str, List[str]], sep: str = "/"):
        """
        搜索以prefix为前缀的所有词
        Args:
            sentence: 前缀句子
            sep:句子中 词之间的分隔符

        Returns:
            返回列表，列表中包含：字典树中所有以prefix作为前缀的词
        """
        if isinstance(sentence, str):
            sentence = sentence.strip().split(sep)

        result = []
        words = []
        current = self.root
        for word in sentence:
            words.append(word)
            current = current.children.get(word)
            if current is None:
                return result
        self._dfs_prefix_sentence(current, words, result)
        return result

    def get_sentences(self) -> List[str]:
        sentence = []
        self._dfs_prefix_sentence(node=self.root, words=[], result=sentence)
        return sentence

    def _dfs_prefix_sentence(self, node, words, result) -> None:
        if node.is_leaf:
            result.append("".join(words))

        for key, value in node.children.items():
            words.append(key)
            self._dfs_prefix_sentence(value, words, result)
            words.pop()

    def merge_trie(self, other_trie):
        for sentence in other_trie.get_sentences():
            self.insert(sentence)


class QueryTrie:

    def __init__(self):
        self.word_freq = {}

    @classmethod
    def from_words(cls, words: Union[List[str], Dict[str, int], List[Tuple[str, int]]]):
        trie = cls()
        if isinstance(words, list) and isinstance(words[0], str):
            for word in words:
                if word not in trie.word_freq:
                    trie.word_freq[word] = 1
                else:
                    trie.word_freq[word] += 1

                # 将子串序列加入字典
                for i in range(len(word), -1, -1):
                    tmp_word = word[:i]
                    if tmp_word not in trie.word_freq:
                        trie.word_freq[tmp_word] = 0

        if isinstance(words, dict):  # 如果传入的是字典 key：word，value：frequency
            for word, freq in words.items():
                if word not in trie.word_freq:
                    trie.word_freq[word] = freq
                else:
                    trie.word_freq[word] += freq

                for i in range(len(word), -1, -1):
                    tmp_word = word[:i]
                    if tmp_word not in trie.word_freq:
                        trie.word_freq[tmp_word] = 0

        if isinstance(words, list) and isinstance(words[0], tuple):
            for word, freq in words:
                if word not in trie.word_freq:
                    trie.word_freq[word] = freq
                else:
                    trie.word_freq[word] += freq

                for i in range(len(word), -1, -1):
                    tmp_word = word[:i]
                    if tmp_word not in trie.word_freq:
                        trie.word_freq[tmp_word] = 0

        return trie

    @classmethod
    def from_file(cls, word_file: Union[str, Path], encoding="utf8",sep="\t"):
        trie = cls()
        word_file = Path(word_file)

        with word_file.open('r',encoding=encoding) as f:
            for line in f:
                splits = line.strip().split(sep)
                if len(splits) > 1:
                    word,freq = splits[0],splits[1]
                    if word not in trie.word_freq:
                        trie.word_freq[word] = freq
                    else:
                        trie.word_freq[word] += freq
                for i in range(len(word),-1,-1):
                    tmp_word = word[:i]
                    if tmp_word not in trie.word_freq:
                        trie.word_freq[tmp_word] = 0
        return trie

    def insert(self,word:Union[str,Tuple[str,int]],sep='\t'):
        if isinstance(word,str) and sep in word:
            word,freq = word.strip().split(sep)
        elif isinstance(word,str):
            freq = 1
        elif isinstance(word,tuple):
            word,freq = word

        if word not in self.word_freq:
            self.word_freq[word] = freq

        for i in range(len(word),-1,-1):
            tmp_word = word[:i]
            if tmp_word not in self.word_freq:
                self.word_freq[tmp_word] = 0

    def search(self,word:str):
        """
        查询word 是否在字典树中
        Args:
            word:

        Returns:
            -1: 表示word 不在字典树中
             0: 表示word是前缀
            >0: 表示word在字典树中，并返回词频

        """
        if word in self.word_freq:
            return self.word_freq[word]
        else:
            return -1
