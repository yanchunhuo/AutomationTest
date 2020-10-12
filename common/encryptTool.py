#-*- coding:utf8 -*-
# 作者 yanchunhuo
# 创建时间 2018/01/19 22:36
# github https://github.com/yanchunhuo
from Crypto.Cipher import AES
import hashlib
import base64

class EncryptTool:

    @classmethod
    def md5Encode(cls,text):
        """
        md5加密，32位
        :param str:
        :return:
        """
        m=hashlib.md5()
        m.update(text.encode('utf-8'))
        return m.hexdigest()

    @classmethod
    def base64Encode(cls,text):
        return base64.b64encode(bytes(text))

    @classmethod
    def base64Decode(cls,base64Text):
        return base64.b64decode(base64Text)

    @classmethod
    def aesEncrypt_with_CBC(cls,text:str,key:str,iv:str):
        """
        AES的CBC模式加密,返回base64
        @param text: 待加密字符串
        @param key: 加密密码
        @param iv: 初始化向量
        @return:
        """
        mode=AES.MODE_CBC
        key=key.encode('utf-8')
        iv=iv.encode('utf-8')
        # 文本用空格补足为16位
        remainder=len(text.encode('utf-8'))%16
        if remainder:
            text=text+'\0'*(16-remainder)
        cipher=AES.new(key,mode,iv)
        cipher_text=cipher.encrypt(text.encode('utf-8'))
        return cls.base64Encode(cipher_text).decode('utf-8')

    @classmethod
    def aesDecrypt_with_CBC(cls,encryptText:str,key:str,iv:str):
        """
        AES的CBC模式解密
        @param encryptText: 待解密字符串,base64
        @param key: 加密密码
        @param iv: 初始化向量
        @return:
        """
        mode=AES.MODE_CBC
        key=key.encode('utf-8')
        iv=iv.encode('utf-8')
        cipher = AES.new(key, mode, iv)
        text=cipher.decrypt(cls.base64Decode(encryptText))
        return text.decode('utf-8')

    @classmethod
    def aesEncrypt_with_ECB(cls, text: str, key: str):
        """
        AES的ECB模式加密,返回base64
        @param text: 待加密字符串
        @param key: 加密密码
        @return:
        """
        mode = AES.MODE_ECB
        key = key.encode('utf-8')
        # 文本用空格补足为16位
        remainder = len(text.encode('utf-8')) % 16
        if remainder:
            text = text + '\0' * (16 - remainder)
        cipher = AES.new(key, mode)
        cipher_text = cipher.encrypt(text.encode('utf-8'))
        return cls.base64Encode(cipher_text).decode('utf-8')

    @classmethod
    def aesDecrypt_with_ECB(cls, encryptText: str, key: str):
        """
        AES的CBC模式解密
        @param encryptText: 待解密字符串,base64
        @param key: 加密密码
        @return:
        """
        mode = AES.MODE_ECB
        key = key.encode('utf-8')
        cipher = AES.new(key, mode)
        text = cipher.decrypt(cls.base64Decode(encryptText))
        return text.decode('utf-8')