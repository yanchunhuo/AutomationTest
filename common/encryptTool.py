#-*- coding:utf8 -*-
# 作者 yanchunhuo
# 创建时间 2018/01/19 22:36
# github https://github.com/yanchunhuo
import hashlib
import base64
class EncryptTool:

    @classmethod
    def md5Encode(cls,str):
        """
        md5加密，32位
        :param str:
        :return:
        """
        m=hashlib.md5()
        m.update(str.encode('utf-8'))
        return m.hexdigest()

    @classmethod
    def base64Encode(cls,str):
        return base64.b64encode(bytes(str))

    @classmethod
    def base64Decode(cls,base64Str):
        return base64.b64decode(base64Str)
