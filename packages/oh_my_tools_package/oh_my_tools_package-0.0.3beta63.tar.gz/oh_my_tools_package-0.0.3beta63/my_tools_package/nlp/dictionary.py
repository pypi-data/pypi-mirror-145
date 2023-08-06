# -*- coding: utf-8 -*-
# @Time    : 2021/11/3 1:37 下午
# @Author  : jeffery
# @FileName: dictionary.py
# @website : http://www.jeffery.ink/
# @github  : https://github.com/jeffery0628
# @Description:
import random
import pypinyin
from copy import deepcopy
from pathlib import Path
from typing import Union, Dict, List
from collections import defaultdict
# from my_tools_package import CONF
from my_tools_package.utils.file import IOUtils


class StatesMachineException(Exception): pass


class Node(object):
    def __init__(self, from_word, to_word=None, is_tail=True,
                 have_child=False):
        self.from_word = from_word
        if to_word is None:
            self.to_word = from_word
            self.data = (is_tail, have_child, from_word)
            self.is_original = True
        else:
            self.to_word = to_word or from_word
            self.data = (is_tail, have_child, to_word)
            self.is_original = False
        self.is_tail = is_tail
        self.have_child = have_child

    def is_original_long_word(self):
        return self.is_original and len(self.from_word) > 1

    def is_follow(self, chars):
        return chars != self.from_word[:-1]

    def __str__(self):
        return '<Node, %s, %s, %s, %s>' % (repr(self.from_word),
                                           repr(self.to_word), self.is_tail, self.have_child)

    __repr__ = __str__


class ConvertMap(object):
    def __init__(self, mapping):
        self._map = {}
        self.set_convert_map(mapping)

    def set_convert_map(self, mapping):
        convert_map = {}
        have_child = {}
        max_key_length = 0
        for key in sorted(mapping.keys()):
            if len(key) > 1:
                for i in range(1, len(key)):
                    parent_key = key[:i]
                    have_child[parent_key] = True
            have_child[key] = False
            max_key_length = max(max_key_length, len(key))
        for key in sorted(have_child.keys()):
            convert_map[key] = (key in mapping, have_child[key],
                                mapping.get(key, ""))
        self._map = convert_map
        self.max_key_length = max_key_length

    def __getitem__(self, k):
        try:
            is_tail, have_child, to_word = self._map[k]
            return Node(k, to_word, is_tail, have_child)
        except:
            return Node(k)

    def __contains__(self, k):
        return k in self._map

    def __len__(self):
        return len(self._map)

    # states


# (START, END, FAIL, WAIT_TAIL) = list(range(4))
# (START, END, FAIL, WAIT_TAIL) = 0，1，2，3
# # conditions
# (TAIL, ERROR, MATCHED_SWITCH, UNMATCHED_SWITCH, CONNECTOR) = list(range(5))

class StatesMachine(object):
    # states: start,end,fail,wait_tail
    START, END, FAIL, WAIT_TAIL = 0, 1, 2, 3
    # condition:tail,error,matched_switch,unmatched_switch,connector
    TAIL, ERROR, MATCHED_SWITCH, UNMATCHED_SWITCH, CONNECTOR = 0, 2, 3, 4, 5

    def __init__(self):
        self.state = self.START
        self.final = ""
        self.len = 0
        self.pool = ""

    def clone(self, pool):
        new = deepcopy(self)
        new.state = self.WAIT_TAIL
        new.pool = pool
        return new

    def feed(self, char, map):
        node = map[self.pool + char]

        if node.have_child:
            if node.is_tail:
                if node.is_original:
                    cond = self.UNMATCHED_SWITCH
                else:
                    cond = self.MATCHED_SWITCH
            else:
                cond = self.CONNECTOR
        else:
            if node.is_tail:
                cond = self.TAIL
            else:
                cond = self.ERROR

        new = None
        if cond == self.ERROR:
            self.state = self.FAIL
        elif cond == self.TAIL:
            if self.state == self.WAIT_TAIL and node.is_original_long_word():
                self.state = self.FAIL
            else:
                self.final += node.to_word
                self.len += 1
                self.pool = ""
                self.state = self.END
        elif self.state == self.START or self.state == self.WAIT_TAIL:
            if cond == self.MATCHED_SWITCH:
                new = self.clone(node.from_word)
                self.final += node.to_word
                self.len += 1
                self.state = self.END
                self.pool = ""
            elif cond == self.UNMATCHED_SWITCH or cond == self.CONNECTOR:
                if self.state == self.START:
                    new = self.clone(node.from_word)
                    self.final += node.to_word
                    self.len += 1
                    self.state = self.END
                else:
                    if node.is_follow(self.pool):
                        self.state = self.FAIL
                    else:
                        self.pool = node.from_word
        elif self.state == self.END:
            # END is a new START
            self.state = self.START
            new = self.feed(char, map)
        elif self.state == self.FAIL:
            raise StatesMachineException('Translate States Machine '
                                         'have error with input data %s' % node)
        return new

    def __len__(self):
        return self.len + 1

    def __str__(self):
        return '<StatesMachine %s, pool: "%s", state: %s, final: %s>' % (
            id(self), self.pool, self.state, self.final)

    __repr__ = __str__


class Converter(object):
    START, END, FAIL, WAIT_TAIL = 0, 1, 2, 3

    def __init__(self, converted_map):
        self.map = converted_map
        self.start()

    def feed(self, char):
        branches = []
        for fsm in self.machines:
            new = fsm.feed(char, self.map)
            if new:
                branches.append(new)
        if branches:
            self.machines.extend(branches)
        self.machines = [fsm for fsm in self.machines if fsm.state != self.FAIL]
        all_ok = True
        for fsm in self.machines:
            if fsm.state != self.END:
                all_ok = False
        if all_ok:
            self._clean()
        return self.get_result()

    def _clean(self):
        if len(self.machines):
            self.machines.sort(key=lambda x: len(x))
            # self.machines.sort(cmp=lambda x,y: cmp(len(x), len(y)))
            self.final += self.machines[0].final
        self.machines = [StatesMachine()]

    def start(self):
        self.machines = [StatesMachine()]
        self.final = ""

    def end(self):
        self.machines = [fsm for fsm in self.machines
                         if fsm.state == self.FAIL or fsm.state == self.END]
        self._clean()

    def convert(self, string):
        self.start()
        for char in string:
            self.feed(char)
        self.end()
        return self.get_result()

    def get_result(self):
        return self.final


def make_dict(text: str) -> defaultdict:
    """将加载的词表转化成字典类型,仅适用于一行只有两个元素"""
    word_map = defaultdict()

    lines = text.split("\n")
    for line in lines:
        splits = line.split("\t")
        if len(splits) > 1:
            word_map[splits[0]] = splits[1]
    return word_map


class Dictionary:

    def __init__(self):
        self.dictionary_dir = Path(CONF["data_dir"]) / "dictionary"
        self.dict_config = IOUtils.read_yaml(CONF["dictionary_config_file"])


    def _download_file(self, url: str, save_path: Union[str, Path] = None) -> str:
        """
        """
        save_path = IOUtils.ensure_dir(save_path) if save_path else IOUtils.ensure_dir(self.dictionary_dir)
        filename = url.split("/")[-1]
        file_path = save_path / filename
        if not file_path.exists():
            file_content = IOUtils.download_file(url)
            file_path = IOUtils.ensure_file(file_path)
            with file_path.open("w") as f:
                f.write(file_content)
        else:
            with file_path.open("r") as f:
                file_content = f.read()
        return file_content

    def _download_file_from_cos(self,bucket:str,key:str,save_path:Union[str, Path] = None)->str:
        """
        从腾讯云上下载文件到本地
        Args:
            bucket:
            key:
            save_path:
        Returns:
        """
        save_path = IOUtils.ensure_dir(save_path) if save_path else IOUtils.ensure_dir(self.dictionary_dir)
        filename = key.split("/")[-1]
        file_path = save_path / filename
        if not file_path.exists():
            IOUtils.download_file_from_cos(bucket,key,str(file_path))
        with file_path.open("r") as f:
            return f.read()

    def load_words(self, save_path: Union[str, Path] = None) -> str:
        """
        从腾讯云上下载 通用分词词典文件
        Args:
            save_path: 文件的保存本地路径
        Returns:
        """
        return self._download_file(self.dict_config["word_freq"]["url"], save_path)

    def load_common_char(self, save_path: Union[str, Path] = None) -> str:
        """
        中文常用字符集(一些常用的汉字)
        Args:
            save_path: 文件的保存本地路径
        Returns:

        """
        return self._download_file(self.dict_config["common_char"]["url"], save_path)

    def load_same_pinyin(self, save_path: Union[str, Path] = None) -> str:
        """
        同音字,其内容：汉字	同音同调	同音异调 。 比如： 八	巴扒捌笆芭疤吧叭	爸靶霸把伯耙罢拔跋坝
        Args:
            save_path: 文件的保存本地路径

        Returns:

        """
        return self._download_file(self.dict_config["same_pinyin"]["url"], save_path)

    def load_same_stroke(self, save_path: Union[str, Path] = None) -> str:
        """
        形似字,其内容, 龚	龛	詟	垄	陇
        Args:
            save_path: 文件的保存本地路径

        Returns:

        """
        return self._download_file(self.dict_config["same_stroke"]["url"], save_path)

    def load_person_name(self, save_path: Union[str, Path] = None) -> str:
        """
        知名人名词典 format: 词语 词频 ,刘德华	5086
        Args:
            save_path: 文件的保存本地路径

        Returns:

        """
        return self._download_file(self.dict_config["person_name"]["url"], save_path)

    def load_place_name(self, save_path: Union[str, Path] = None) -> str:
        """
        地名词典 format: 词语 词频 ,  酒店	201212
        Args:
            save_path:

        Returns:

        """
        return self._download_file(self.dict_config["place_name"]["url"], save_path)

    def load_stop_words(self, save_path: Union[str, Path] = None) -> str:
        """
        停用词
        Args:
            save_path:

        Returns:

        """

        return self._download_file(self.dict_config["stop_words"]["url"], save_path)

    def load_en_word_freq(self, save_path: Union[str, Path] = None) -> str:
        """
        英文拼写词频文件
        Args:
            save_path:

        Returns:

        """
        return self._download_file(self.dict_config["en_word_freq"]["url"], save_path)

    def load_wechat_expression(self, save_path: Union[str, Path] = None) -> str:
        """微信表情  代码 转 文字"""
        return self._download_file(self.dict_config["wechat_expression"]["url"], save_path)

    def load_traditional2simple(self, save_path: Union[str, Path] = None) -> str:
        return self._download_file(self.dict_config["traditional2simple"]["url"], save_path)

    def load_simple2traditional(self, save_path: Union[str, Path] = None) -> str:
        return self._download_file(self.dict_config["simple2traditional"]["url"], save_path)

    def sample_with_freq(self, input_dict):
        """
        基于频率采样
        输入的形式为：`{word1:2, word2:3, word3:1}`，其中键表示要采样的值，值表示对应出现的次数。要求按照频率每次随机输出一个采样值。

        Args:
            input_dict:{word1:2, word2:3, word3:1}

        Returns:

        """
        keys = list(input_dict.keys())
        values = list(input_dict.values())

        sum_values = sum(values)
        # 计算概率
        probas = []
        for v in values:
            probas.append(v / sum_values)

        # 产生随机数
        rand = random.uniform(0, 1)
        # 累积概率
        cum_proba = 0
        for value, proba in zip(values, probas):
            cum_proba += proba
            if cum_proba >= rand:
                return value

    def get_homophones_by_char(self, input_char: str) -> List[str]:
        """取字符 input_char 的所有同音字"""
        result = []
        # CJK统一汉字区的范围是0x4E00-0x9FA5,也就是我们经常提到的20902个汉字
        for i in range(0x4e00, 0x9fa6):
            if pypinyin.core.pinyin([chr(i)], style=pypinyin.NORMAL, strict=False)[0][0] == \
                    pypinyin.core.pinyin(input_char, style=pypinyin.NORMAL, strict=False)[0][0]:
                result.append(chr(i))
        return result

    def get_homophones_by_pinyin(self, input_pinyin) -> List[str]:
        """根据拼音取所有同音字"""
        result = []
        # CJK统一汉字区的范围是0x4E00-0x9FA5,也就是我们经常提到的20902个汉字
        for i in range(0x4e00, 0x9fa6):
            if pypinyin.core.pinyin([chr(i)], style=pypinyin.NORMAL, strict=False)[0][0] == input_pinyin:
                result.append(chr(i))
        return result

    @property
    def stop_words(self) -> Dict[str, int]:
        """停用词表"""
        file_content = self.load_stop_words()
        stop_words = defaultdict(int)
        for word in set(file_content.split("\n")):
            stop_words[word.strip()] += 1
        return stop_words

    @property
    def common_char(self) -> List[str]:
        """中文从常见的3502个汉字"""
        file_content = self.load_common_char()
        common_chars = []
        for char in file_content.split('\n'):
            common_chars.append(char.strip())
        return common_chars

    @property
    def same_stroke(self) -> Dict[str, List[str]]:
        file_content = self.load_same_stroke()
        word_stroke = defaultdict(list)
        for word_same in file_content.split("\n"):
            if not word_same.strip():
                continue
            word, stroke_word_str = word_same.split("\t")
            if stroke_word_str.strip():
                same_stroke_words = stroke_word_str.split(",")
            else:
                same_stroke_words = []
            word_stroke[word] = same_stroke_words
        return word_stroke

    @property
    def same_pinyin(self) -> Dict[str, Dict[str, List[str]]]:
        file_content = self.load_same_pinyin()
        word_pinyin_dict = defaultdict(dict)
        for line in file_content.split("\n"):
            splits = line.split("\t")
            if not len(splits) == 3:
                continue
            word_pinyin_dict[splits[0]] = {
                "homonym": splits[1].strip().split(",") if splits[1].strip() else [],
                "difference": splits[2].strip().split(",") if splits[2].strip() else []
            }
        return word_pinyin_dict






