#!-*- coding:utf8 -*-
import re
import uuid
import json
import random
import string

class StrTool:

    letters = list(string.ascii_letters)
    whitespace = list(string.whitespace)
    punctuation = list(string.punctuation)
    digits = list(string.digits)
    # 汉字编码的范围
    ch_start = 0x4E00
    ch_end = 0x9FA5

    @classmethod
    def getStringWithLBRB(cls, sourceStr, lbStr, rbStr, offset=0):
        """
        根据字符串左右边界获取内容
        offset:要获得匹配的第几个数据,默认第一个
        :param sourceStr:
        :param lbStr:
        :param rbStr:
        :param offset:
        :return:
        """
        regex = '([\\s\\S]*?)'
        r = re.compile(lbStr + regex + rbStr)
        result = r.findall(sourceStr)
        if str(offset) == 'all':
            return result
        else:
            if len(result) >= offset and len(result) != 0:
                return result[offset]
            else:
                return None

    @classmethod
    def addUUID(cls,source):
        """
        字符串加上uuid
        :param source:
        :return:
        """
        return source+'_'+str(uuid.uuid4())

    @classmethod
    def objectToJsonStr(cls,object):
        """
        将类对象转为json字符串
        :param object:
        :return:
        """
        return json.dumps(object, default=lambda obj: obj.__dict__)

    @classmethod
    def objectToJson(cls,object):
        """
        将类对象转为json
        :param object:
        :return:
        """
        return json.loads(json.dumps(object, default=lambda obj: obj.__dict__))

    @classmethod
    def getSpecifiedStr(cls,length,char):
        """
        根据字符获取指定长度的字符串
        :param length:
        :param char:
        :return:
        """
        result=''
        for i in range(int(length)):
            result=result+str(char)
        return result

    @classmethod
    def getRandomChar(cls):
        """
        随机获取a-zA-Z的单个字符
        :return:
        """
        str=string.ascii_letters
        return random.choice(str)

    @classmethod
    def random_index(cls, percents):
        """
        随机变量的概率函数,返回概率事件的下标索引
        :return:
        """
        start = 0
        index = 0
        randnum = random.randint(1, sum(percents))

        for index, scope in enumerate(percents):
            start += scope
            if randnum <= start:
                break
        return index

    @classmethod
    def getRandomText(cls, length, ch_percent=90, en_percent=5, digits_percent=3, punctuation_percent=2,
                      whitespace_percent=0):
        """
        获取指定长度文本内容，可设置中文、英文、数字、标点符号、空白字符现的概率
        如果字符串包含中文，返回的内容为Unicode
        :param length: 生成文本的长度
        :param ch_percent: 出现中文字符的概率
        :param en_percent: 出现英文字符的概率
        :param digits_percent: 出现数字字符的概率
        :param punctuation_percent: 出现标点符号的概率
        :param whitespace_percent: 出现空白字符的概率
        :return:
        """
        percents = [ch_percent, en_percent, digits_percent, punctuation_percent, whitespace_percent]
        percents_info = ['ch_percent', 'en_percent', 'digits_percent', 'punctuation_percent', 'whitespace_percent']
        result = ''
        for i in range(length):
            info = percents_info[cls.random_index(percents)]
            if info == 'ch_percent':
                result += chr(random.randint(int(cls.ch_start), int(cls.ch_end)))
            elif info == 'en_percent':
                result += random.choice(cls.letters)
            elif info == 'digits_percent':
                result += random.choice(cls.digits)
            elif info == 'punctuation_percent':
                result += random.choice(cls.punctuation)
            elif info == 'whitespace_percent':
                result += random.choice(cls.whitespace)
        return result