# -*- coding:utf8 -*-
# 作者 yanchunhuo
# 创建时间 2018/01/19 22:36
# github https://github.com/yanchunhuo
import base64
import hashlib
from typing import Union

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
    def base64_encode(cls,data:Union[str,bytes],encoding='utf-8'):
        """_summary_

        Args:
            data (Union[str | bytes]): 需要编码的数据
            encoding (str, optional): 当data为text时生效. Defaults to 'utf-8'.

        Returns:
            _type_: _description_
        """
        if isinstance(data,str):
            data=bytes(data,encoding=encoding)
        return base64.b64encode(data).decode('utf-8')

    @classmethod
    def base64_decode(cls,base64_text:str):
        return base64.b64decode(base64_text)
    
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
