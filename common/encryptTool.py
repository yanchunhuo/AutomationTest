#-*- coding:utf8 -*-
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
