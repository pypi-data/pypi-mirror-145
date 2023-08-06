# -*- coding: utf-8 -*-
# @Time    : 2021/9/28 9:20 上午
# @Author  : jeffery
# @FileName: strings.py
# @website : http://www.jeffery.ink/
# @github  : https://github.com/jeffery0628
# @Description:

# # 最长公共子序列
# from my_tools_package.algorithm.lcs import lcs_length, lcs_string, lcs_strings
#
# # levenshtein编辑距离
# from my_tools_package.algorithm.levenshtein import levenshtein_distance
#
# # 字典树
# from my_tools_package.algorithm.trie import TrieNode, CharTrie, StringTrie
#
# # 字符串查找算法：KMP算法、Boyer-Moore算方法、rabin_karp指纹算法
# from my_tools_package.algorithm.kmp import kmp_next, kmp_search
# from my_tools_package.algorithm.boyer_moore import generate_good_suffix, generate_bad_character, boyer_moore
# from my_tools_package.algorithm.rabin_karp import rabin_karp
import regex as re
from pathlib import Path

import pypinyin
from typing import List, Union

from my_tools_package.nlp.dictionary import Dictionary, make_dict
from my_tools_package.nlp.dictionary import ConvertMap, Converter


class StringUtils:

    def __init__(self):
        self.dictionary = Dictionary()

        self._initialize_puncs()

    def _initialize_puncs(self):
        """初始化标点符号规则"""

        self._CNPuncs = ['。', '，', '！', '？', '、', '；', '：', '“',
                         '”', '‘', '’', '（', '）', '【', '】', '{', '}',
                         '『', '』', '「', '」', '〔', '〕', '——', '……', '—', '-',
                         '～', '·', '《', '》', '〈', '〉', '﹏', '___', '.']
        self._CNPuncs_rule = re.compile("[。，！？、；：“”‘’（）【】\{\}『』「」〔〕——……—\-～·《》〈〉﹏___\.]")

        self._ENPuncs = [',', '.', '"', ':', ')', '(', '-', '!', '?', '|', ';', "'", '$', '&', '/',
                         '[', ']', '>', '%', '=', '#', '*', '+', '\\', '•', '~', '@', '£', '·', '_',
                         '{', '}', '©', '^', '®', '`', '<', '→', '°', '€', '™', '›', '♥', '←', '×',
                         '§', '″', '′', 'Â', '█', '½', 'à', '…', '“', '★', '”', '–', '●', 'â', '►',
                         '−', '¢', '²', '¬', '░', '¶', '↑', '±', '¿', '▾', '═', '¦', '║', '―', '¥',
                         '▓', '—', '‹', '─', '▒', '：', '¼', '⊕', '▼', '▪', '†', '■', '’', '▀', '¨',
                         '▄', '♫', '☆', 'é', '¯', '♦', '¤', '▲', 'è', '¸', '¾', 'Ã', '⋅', '‘', '∞',
                         '∙', '）', '↓', '、', '│', '（', '»', '，', '♪', '╩', '╚', '³', '・', '╦', '╣',
                         '╔', '╗', '▬', '❤', 'ï', 'Ø', '¹', '≤', '‡', '√', ]
        self._ENPuncs_rule = re.compile(
            "[,\.\":\)\(\-!\?\|;'\$&/\[\]>%=#\*\+\\•~@£·_\{\}©\^®`<→°€™›♥←×§″′Â█½à…“★”–●â►−¢²¬░¶↑±¿▾═¦║―¥▓—‹─▒：¼⊕▼▪†■’▀¨▄♫☆é¯♦¤▲è¸¾Ã⋅‘∞∙）↓、│（»，♪╩╚³・╦╣╔╗▬❤ïØ¹≤‡√]")

    @classmethod
    def is_alphabet(cls, uchar: str):
        """
        判断一个unicode是否是英文字母
        Args:
            uchar: 字符

        Returns:

        """

        placesym = {u'{', u'}', u'[', u']', u'-', u'_'}
        return ('\u0041' <= uchar <= '\u005a') or ('\u0061' <= uchar <= '\u007a') or (uchar in placesym)

    @classmethod
    def is_alphabet_string(cls, string: str):
        """
        判断是否全部为英文字母
        Args:
            string: 字符串

        Returns:

        """
        return all(cls.is_alphabet(c) for c in string)

    @classmethod
    def is_chinese_char(cls, ch):
        """Checks whether CP is the codepoint of a CJK character."""
        # This defines a "chinese character" as anything in the CJK Unicode block:
        #   https://en.wikipedia.org/wiki/CJK_Unified_Ideographs_(Unicode_block)
        cp = ord(ch)
        if ((0x4E00 <= cp <= 0x9FFF) or  #
                (0x3400 <= cp <= 0x4DBF) or  #
                (0x20000 <= cp <= 0x2A6DF) or  #
                (0x2A700 <= cp <= 0x2B73F) or  #
                (0x2B740 <= cp <= 0x2B81F) or  #
                (0x2B820 <= cp <= 0x2CEAF) or
                (0xF900 <= cp <= 0xFAFF) or  #
                (0x2F800 <= cp <= 0x2FA1F)):  #
            return True

        return False

    @classmethod
    def is_chinese_string(cls, string: str):
        """
        判断字符串是否全为汉字
        Args:
            string:字符串

        Returns:

        """
        return all(cls.is_chinese_char(c) for c in string)

    @classmethod
    def is_number(cls, uchar: str):
        """
        判断一个unicode是否是数字
        Args:
            uchar: 字符

        Returns:

        """
        return '\u0030' <= uchar <= '\u0039'

    @classmethod
    def is_number_string(cls, string: str):
        """判断字符串是否全为数字"""
        return all(cls.is_number(c) for c in string)

    @classmethod
    def convert_to_unicode(cls, text) -> str:
        """
        字符串将编码后的不可阅读的内容转化为可阅读字符串
        Args:
            text: 文本字符串

        Returns:

        """
        if isinstance(text, str):
            return text
        elif isinstance(text, bytes):
            try:
                text = text.decode('utf-8')
            except UnicodeDecodeError:
                text = text.decode('gbk', 'ignore')
            return text
        else:
            raise ValueError("Unsupported string type: %s" % (type(text)))

    @classmethod
    def full2half_char(cls, uchar):
        """全角转半角"""
        inside_code = ord(uchar)
        if inside_code == 0x3000:  # 全角空格直接转换
            inside_code = 0x0020
        else:
            inside_code -= 0xfee0  # 全角字符（除空格）根据对应的关系转换
        if inside_code < 0x0020 or inside_code > 0x7e:  # 转完之后不是半角字符返回原来的字符
            return uchar
        return chr(inside_code)

    @classmethod
    def full2half(cls, text: str):
        """
        将字符串文本全角转半角处理
        Args:
            text: 字符串文本

        Returns:返回转换后的文本字符串

        """
        res = []
        for c in text:
            res.append(cls.full2half_char(c))
        return "".join(res)

    @classmethod
    def half2full_char(cls, uchar: str) -> str:
        """半角转全角"""
        inside_code = ord(uchar)
        if inside_code < 0x0020 or inside_code > 0x7e:  # 不是半角字符就返回原来的字符
            return uchar
        if inside_code == 0x0020:  # 除了空格其他的全角半角的公式为:半角=全角-0xfee0
            inside_code = 0x3000
        else:
            inside_code += 0xfee0
        return chr(inside_code)

    @classmethod
    def half2full(cls, text: str) -> str:
        """
        将字符串文本半角字符转全角处理
        Args:
            text: 输入文本

        Returns:返回转换后的文本

        """
        res = []
        for c in text:
            res.append(StringUtils.half2full_char(c))
        return "".join(res)

    def _remove_stop_words(self, tokens: List[str]) -> List[str]:

        return [_ for _ in tokens if _ not in self.dictionary.stop_words]

    @classmethod
    def remove_stop_words(cls, tokens: List[str]) -> List[str]:
        """
        去除停用词
        Args:
            tokens: 分词结果

        Returns: 返回去除停用词的分词结果

        """
        return cls()._remove_stop_words(tokens)

    def _remove_chinese_punctuation(self, tokens: List[str]) -> List[str]:
        """去除分词后的中文标点符号"""
        return [_ for _ in tokens if _ not in self._CNPuncs]

    @classmethod
    def remove_chinese_punctuation(cls, tokens: List[str]) -> List[str]:
        """去除分词后的中文标点符号"""
        return cls()._remove_chinese_punctuation(tokens)

    def _remove_english_punctuation(self, tokens: List[str]) -> List[str]:
        """去除分词后的英文标点符号"""
        return [_ for _ in tokens if _ not in self._ENPuncs]

    @classmethod
    def remove_english_punctuation(cls, tokens: List[str]) -> List[str]:
        """去除英文标点符号"""
        return cls()._remove_english_punctuation(tokens)

    def _remove_punctuation(self, tokens: List[str]) -> List[str]:
        """去除分词后的标点符号"""
        return [_ for _ in tokens if _ not in self._CNPuncs + self._ENPuncs]

    @classmethod
    def remove_punctuation(cls, tokens: List[str]) -> List[str]:
        """去除分词后的标点符号"""
        return cls()._remove_punctuation(tokens)

    @classmethod
    def escape_re_character(cls, s: str) -> str:
        """对正则字符添加转义"""
        escape_char = ["\\", "\"", "*", ".", "?", "+", "$", "^", "[", "]", "(", ")", "{", "}", "|", "-"]
        for c in escape_char:
            if c in s:
                s = s.replace(c, re.escape(c))
        return s

    @classmethod
    def remove_string_punc(cls, s: str) -> str:
        """去除字符串中的标点符号"""
        string_utils = cls()
        s = string_utils._CNPuncs_rule.sub("", s)
        s = string_utils._ENPuncs_rule.sub("", s)
        return s

    @classmethod
    def wechat_expression_2_word(cls, text: str) -> str:
        """将文本中的微信表情代码转化成文字"""
        code_expression = make_dict(cls().dictionary.load_wechat_expression())
        for key, value in code_expression.items():
            text = text.replace(key, value)

        return text

    @classmethod
    def traditional2simple(cls, text: str) -> str:
        """将繁体字符串转化为简体字符串"""
        word_map = make_dict(cls().dictionary.load_traditional2simple())
        return Converter(ConvertMap(word_map)).convert(text)

    @classmethod
    def simple2traditional(cls, text: str) -> str:
        """将简体字符串转化为繁体字符串"""
        word_map = make_dict(cls().dictionary.load_simple2traditional())
        return Converter(ConvertMap(word_map)).convert(text)

    @classmethod
    def text2pinyin(cls, text: str, with_tone: bool = False) -> List[str]:
        """
        将文本字符串转成拼音
        Args:
            text: 输入的文本字符串
            with_tone: 是否对转化的拼音加上声调

        Returns:

        """

        result = pypinyin.core.pinyin(text, strict=False, style=pypinyin.TONE if with_tone else pypinyin.NORMAL)
        return [_[0] for _ in result]

    @classmethod
    def get_homophones_by_char(cls, input_char: str) -> List[str]:
        """
        取汉字 input_char 的所有同音字
        Args:
            input_char:

        Returns:
        """
        return cls().dictionary.get_homophones_by_char(input_char)

    @classmethod
    def get_homophones_by_pinyin(cls, input_pinyin: str) -> List[str]:
        """
        根据拼音取所有同音字
        Args:
            input_pinyin:

        Returns:

        """
        return cls().dictionary.get_homophones_by_pinyin(input_pinyin)

    @classmethod
    def parse_old_friends(cls):
        source_dir = Path("/Users/lizhen/Downloads/01")
        source_files = list(source_dir.glob("*.chs&eng.ass"))
        source_files.sort()
        ch_rule = re.compile("(?<=b0\}).*?(?=\{)")

        for source_file in source_files:
            with source_file.open("r",encoding="utf8") as f:
                out_file = source_dir / (source_file.name.split(".")[1]+".txt")
                out_writer = out_file.open("w",encoding="utf8")
                for line in f:
                    target_strs = ch_rule.findall(line)
                    if len(target_strs)>1:
                        out_writer.write(f"{target_strs[1]}\n{target_strs[0]}\n\n")

                out_writer.close()




if __name__ == '__main__':
    print(StringUtils.parse_old_friends())
