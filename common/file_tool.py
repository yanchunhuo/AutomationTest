#!-*- coding:utf8 -*-
# 作者 yanchunhuo
# 创建时间 2018/01/19 22:36
# github https://github.com/yanchunhuo
import ujson
import os
import re
# requests库依赖会安装charset_normalizer
from charset_normalizer import detect

class FileTool:

    @classmethod
    def getChardet(cls,filePath):
        """
        获取文件编码格式，比如utf-8、GB2312
        :param filePath:
        :return:
        """
        with open(filePath, 'rb') as f:
            cur_encoding = detect(f.read())['encoding']
            f.close()
        return cur_encoding

    @classmethod
    def writeObjectIntoFile(cls,obj,filePath,encoding='utf-8'):
        """
        将对象转为json字符串，写入到文件
        :param obj:
        :param filePath:
        :return:
        """
        str = ujson.dumps(obj)
        with open(filePath,'w',encoding=encoding) as f:
            f.write(str)
            f.close()

    @classmethod
    def readJsonFromFile(cls,filePath,encoding='utf-8'):
        """
        从文件里读取json字符串
        :param filePath:
        :return:
        """
        with open(filePath,'r',encoding=encoding) as f:
            result=f.read()
            f.close()
        result=ujson.loads(result)
        return result

    @classmethod
    def truncateFile(cls,fielPath,encoding='utf-8'):
        """
        清空文件
        :param fielPath:
        :return:
        """
        with open(fielPath,'r+',encoding=encoding) as f:
            f.truncate()
            f.close()

    @classmethod
    def truncateDir(cls,dirPath,regexs=None):
        """
        清空整个目录的内容
        :param dirPath:
        :param regexs: 正则匹配的文件名，以数组存放多个正则表达式
        :return:
        """
        for path,dirs,files in os.walk(dirPath):
            for file in files:
                filePath=os.path.join(path,file)
                if regexs:
                    pattern = '|'.join(regexs)
                    if re.match(pattern,file):
                        os.remove(filePath)
                else:
                    os.remove(filePath)

    @classmethod
    def replaceFileLineContent(cls, filePath, match_keyword, old, new,encoding='utf-8'):
        """
        根据关键字匹配文档中的行，对行内容进行替换
        :param filePath: 文档路径
        :param match_keyword: 用于匹配文档中包含的关键字行
        :param old: 匹配的行中包含的字符串
        :param new: 用于替换匹配的行中的旧字符串
        :return:
        """
        with open(filePath, 'r',encoding=encoding) as f:
            new_lines = []
            lines = f.readlines()
            for line in lines:
                if match_keyword in line:
                    line = line.replace(old, new)
                new_lines.append(line)
            f.close()

            with open(filePath, 'w+',encoding=encoding) as f:
                f.writelines(new_lines)
                f.close()

    @classmethod
    def replaceFileContent(cls, filePath, old, new, replaceNum=-1, replaceOffset=0,encoding='utf-8'):
        """
        替换文档中的内容,支持替换全部、替换指定前几个、替换第N个
        :param filePath: 文档路径
        :param old: 要替换的字符串
        :param new: 要替换的新字符串
        :param replaceNum: 从头开始替换。-1代表替换所有；-2代表该参数无效，replaceOffset参数生效
        :param replaceOffset: 替换第几个，下标从0开始，
        :return:
        """
        with open(filePath, 'r',encoding=encoding) as f:
            content = f.read()
            if int(replaceNum) == -1:
                content = content.replace(old, new)
            elif not int(replaceNum) == -2:
                # 参数为整数
                replaceNum = abs(replaceNum)
                content = re.sub(old, new, content, replaceNum)
            else:
                # 参数为-2
                index = 0
                # 存储查找到的次数
                times = 0
                while True:
                    # 第一次查找匹配所在的位置
                    if index == 0:
                        index = content.find(old)
                        if index == -1:
                            break
                        else:
                            times = times + 1
                    else:
                        # 从上一次匹配的位置开始查找下一次匹配的位置
                        index = content.find(old, index + 1)
                        if index == -1:
                            break
                        else:
                            times = times + 1

                    if times == int(replaceOffset) + 1:
                        preContent = content[:index]
                        centerContent = new
                        suffContent = content[index + len(old):]
                        content = preContent + centerContent + suffContent
                        break

            with open(filePath, 'w+',encoding=encoding) as f:
                f.writelines(content)
                f.close()

    @classmethod
    def replaceFileContentWithLBRB(cls, filePath, new, lbStr, rbStr, replaceOffset=0,encoding='utf-8'):
        """
        根据左右字符串匹配要替换的文档内容，支持多处匹配只替换一处的功能
        :param filePath: 文档路径
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
        with open(filePath, 'r',encoding=encoding) as f:
            content = f.read()
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
            f.close()

            with open(filePath, 'w+',encoding=encoding) as f:
                f.writelines(content)
                f.close()

    @classmethod
    def appendContent(cls, filePath, content,encoding='utf-8'):
        with open(filePath, 'a',encoding=encoding) as f:
            f.write(content)
            f.close()