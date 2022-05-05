#!-*- coding:utf8 -*-
# 作者 yanchunhuo
# 创建时间 2018/01/19 22:36
# github https://github.com/yanchunhuo
import ujson
import re
import random
import string
import uuid

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
    def addUUID(cls,prefix:str=None,suffix:str=None,separator:str='_'):
        """_summary_

        Args:
            prefix (_type_, optional): _description_. Defaults to None.
            suffix (_type_, optional): _description_. Defaults to None.
            separator (str, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """
        result=str(uuid.uuid4())
        if prefix:
            result=prefix+separator+result
        if suffix:
            result=result+separator+suffix
        return result

    @classmethod
    def objectToJsonStr(cls, object):
        """
        将类对象转为json字符串
        :param object:
        :return:
        """
        import json
        return json.dumps(object,default=lambda o: o.__dict__)

    @classmethod
    def objectToJson(cls, object):
        """
        将类对象转为json
        :param object:
        :return:
        """
        import json
        return ujson.loads(json.dumps(object,default=lambda o: o.__dict__))

    @classmethod
    def getSpecifiedStr(cls, length, char):
        """
        根据字符获取指定长度的字符串
        :param length:
        :param char:
        :return:
        """
        result = ''
        for i in range(int(length)):
            result = result + str(char)
        return result

    @classmethod
    def addFix(cls, sourceStr, isPre=False, preStr='', isSuffix=False, suffixStr=''):
        """
        字符串加前后缀
        :param sourceStr:
        :param isPre:
        :param preStr:
        :param isSuffix:
        :param suffixStr:
        :return:
        """
        preStr = str(preStr).strip()
        suffixStr = str(suffixStr).strip()
        if isPre and isSuffix:
            return '{}{}{}'.format(preStr, sourceStr, suffixStr)
        elif isSuffix:
            return '{}{}'.format(sourceStr, suffixStr)
        elif isPre:
            return '{}{}'.format(preStr, sourceStr)
        else:
            return sourceStr

    @classmethod
    def getRandomChar(cls):
        """
        随机获取a-zA-Z的单个字符
        :return:
        """
        str = string.ascii_letters
        return random.choice(str)

    @classmethod
    def replaceContentWithLBRB(cls, content, new, lbStr, rbStr, replaceOffset=0):
        """
        根据左右字符串匹配要替换的内容，支持多处匹配只替换一处的功能
        :param content:
        :param new: 要替换的新字符串
        :param lbStr: 要替换内容的左侧字符串
        :param rbStr: 要替换内容的右侧字符串
        :param replaceOffset: 需要将第几个匹配的内容进行替换，下标从0开始，所有都替换使用-1
        :return:
        """
        if lbStr == '' and rbStr == '':
            return
        regex = '([\\s\\S]*?)'
        r = re.compile(lbStr + regex + rbStr)

        match_results = r.findall(content)
        if int(replaceOffset) == -1:
            for result in match_results:
                # 为了防止匹配的内容在其他地方也有被替换掉，故需要将匹配的前后字符串加上
                content = content.replace(lbStr + result + rbStr, lbStr + new + rbStr)
        elif len(match_results) >= replaceOffset and len(match_results) != 0:
            # 用于记录匹配到关键字的位置
            index = None
            for i in range(len(match_results)):
                if i == 0:
                    # 第一次查找匹配所在的位置
                    index = content.find(lbStr + match_results[i] + rbStr)
                else:
                    # 从上一次匹配的位置开始查找下一次匹配的位置
                    index = content.find(lbStr + match_results[i] + rbStr, index + 1)
                if i == int(replaceOffset):
                    preContent = content[:index]
                    centerContent = lbStr + new + rbStr
                    suffContent = content[index + len(lbStr + match_results[i] + rbStr):]
                    content = preContent + centerContent + suffContent
                    break
        return content

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

    @classmethod
    def contentToDict(cls, content: str,result_enter_type:str='\r\n'):
        """
        将包含换行符的字符串内容转为字典，目前仅支持格式:key=value
        @param content:
        @param result_enter_type:存储的换行类型，包括\r\n、\n、\r
        @return: {‘key’:{'value':value,'desc':desc}}
        """
        content = content.replace('\r\n', '\n')
        lines = content.split('\n')
        result_dict = {}
        tmp_key_desc=''
        for i,line in enumerate(lines):
            if not line.startswith('#') and not line.startswith('//') and '=' in line:
                tmp_line = line.split('=')
                result_dict.update({tmp_line[0].strip(): {'value':tmp_line[1].strip(),'desc':tmp_key_desc}})
                tmp_key_desc=''
            else:
                tmp_key_desc+=line
                if not i==len(lines)-1:
                    tmp_key_desc+=result_enter_type
        return result_dict

    @classmethod
    def dictToContent(cls, content_dict:dict,result_enter_type:str='\r\n'):
        """
        将def contentToDict(cls, content: str,result_enter_type:str='\r\n')返回的结果拼接为content
        key和value使用=拼接
        @param content_dict:
        @param result_enter_type:存储的换行类型，包括\r\n、\n、\r
        @return:
        """
        result_content = ''
        for key in content_dict.keys():
            result_content += content_dict[key]['desc']
            result_content += key
            result_content += '='
            result_content += content_dict[key]['value']
            result_content += result_enter_type
        return result_content