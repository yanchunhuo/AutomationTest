#-*- coding:utf8 -*-
import re
import filecmp
import os

class AssertTool:
    @classmethod
    def isRegularMatch(cls,sourceStr,regularStr):
        """
        判断字符串是否符合正则表达式，正则表达式的内容包含正则关键字需用\进行转移
        :param sourceStr:
        :param regularStr:
        :return:
        """
        if re.match(regularStr,sourceStr):
            return True
        else:
            return False

    @classmethod
    def isFilesEqual(cls,filePath1,filePath2):
        """
        比较两个文件内容是否一样
        :param filePath1:
        :param filePath2:
        :return:
        """
        if filecmp.cmp(filePath1,filePath2):
            return True
        else:
            return False

    @classmethod
    def isFilesSizeEqual(cls,filePath1,filePath2):
        """
        比较两个文件大小是否一致
        :param filePath2:
        :param filePath1:
        :return:
        """
        size1=os.path.getsize(filePath1)
        size2=os.path.getsize(filePath2)
        if size1==size2:
            return True
        else:
            return False