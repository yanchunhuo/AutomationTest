# -*- coding:utf8 -*-
# 作者 yanchunhuo
# 创建时间 2018/01/19 22:36
# github https://github.com/yanchunhuo
import base64
import hashlib

class BaseEncryptTool:
    
    @classmethod
    def md5Encode(cls, text):
        """
        md5加密，32位
        :param str:
        :return:
        """
        m=hashlib.md5()
        m.update(text.encode('utf-8'))
        return m.hexdigest()
    
    @classmethod
    def base64Encode(cls,text,encoding='utf-8'):
        return base64.b64encode(bytes(text,encoding=encoding))

    @classmethod
    def base64Decode(cls,base64Text):
        return base64.b64decode(base64Text)
    
    @classmethod
    def hash_code(cls, text: str):
        h = 0
        if len(text) > 0:
            for item in text:
                h = 31 * h + ord(item)
            return h
        else:
            return 0
    
    @classmethod
    def sha1Encode(cls, src_str):
        """
        sha1加密
        :param src_str:
        :return desc_str:
        """
        return hashlib.sha1(src_str.encode('utf-8')).hexdigest()
