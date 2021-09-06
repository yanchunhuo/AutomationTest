#
# aes_tool.py
# @author yanchunhuo
# @description 
# @created 2021-09-06T18:28:10.458Z+08:00
# @last-modified 2021-09-06T19:02:54.219Z+08:00
# github https://github.com/yanchunhuo
from Crypto.Cipher import AES
import base64

class AES_Tool:
    def __init__(self,key:str,iv:str) -> None:
        """[summary]

        Args:
            key (str): 加密密码
            iv (str): 初始化向量
        """
        self.key=key.encode('utf-8')
        self.iv=iv.encode('utf-8')
    
    def aes_encrypt_cbc(self,text:str):
        """
        AES的CBC模式加密,返回base64
        @param text: 待加密字符串
        @return:
        """
        mode=AES.MODE_CBC
        # 文本用空格补足为16位
        remainder=len(text.encode('utf-8'))%16
        if remainder:
            text=text+'\0'*(16-remainder)
        cipher=AES.new(self.key,mode,self.iv)
        cipher_text=cipher.encrypt(text.encode('utf-8'))
        return base64.b64encode(cipher_text).decode('utf-8')

    def aes_decrypt_cbc(self,encryptText:str):
        """
        AES的CBC模式解密
        @param encryptText: 待解密字符串,base64
        @return:
        """
        mode=AES.MODE_CBC
        cipher = AES.new(self.key, mode, self.iv)
        text=cipher.decrypt(base64.b64decode(encryptText))
        return text.decode('utf-8')

    def aes_encrypt_ecb(self, text: str):
        """
        AES的ECB模式加密,返回base64
        @param text: 待加密字符串
        @param key: 加密密码
        @return:
        """
        mode = AES.MODE_ECB
        # 文本用空格补足为16位
        remainder = len(text.encode('utf-8')) % 16
        if remainder:
            text = text + '\0' * (16 - remainder)
        cipher = AES.new(self.key, mode)
        cipher_text = cipher.encrypt(text.encode('utf-8'))
        return base64.b64encode(cipher_text).decode('utf-8')

    def aes_decrypt_ecb(self, encryptText: str):
        """
        AES的CBC模式解密
        @param encryptText: 待解密字符串,base64
        @param key: 加密密码
        @return:
        """
        mode = AES.MODE_ECB
        cipher = AES.new(self.key, mode)
        text = cipher.decrypt(base64.b64decode(encryptText))
        return text.decode('utf-8')