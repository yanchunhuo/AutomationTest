#
# aes_tool.py
# @author yanchunhuo
# @description 
# @created 2021-09-06T18:28:10.458Z+08:00
# @last-modified 2023-09-05T18:11:41.678Z+08:00
# github https://github.com/yanchunhuo
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad
import base64
from typing import Union

class AESTool:
    def __init__(self,key:str,iv:str=None) -> None:
        """[summary]

        Args:
            key (str): 加密密码
            iv (str): 初始化向量
        """
        self.key=key.encode('utf-8')
        if iv:
            self.iv=iv.encode('utf-8')
    
    def encrypt_cbc(self,text:str):
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
        encrypted_text=cipher.encrypt(text.encode('utf-8'))
        return base64.b64encode(encrypted_text).decode('utf-8')

    def decrypt_cbc(self,encrypted_text:str):
        """
        AES的CBC模式解密
        @param encrypted_text: 待解密字符串,base64
        @return:
        """
        mode=AES.MODE_CBC
        cipher = AES.new(self.key, mode, self.iv)
        text=cipher.decrypt(base64.b64decode(encrypted_text))
        return text.decode('utf-8')

    def encrypt_ecb(self, text: str):
        """
        AES的ECB模式加密,返回base64
        @param text: 待加密字符串
        @return:
        """
        mode = AES.MODE_ECB
        # 文本用空格补足为16位
        remainder = len(text.encode('utf-8')) % 16
        if remainder:
            text = text + '\0' * (16 - remainder)
        cipher = AES.new(self.key, mode)
        encrypted_text = cipher.encrypt(text.encode('utf-8'))
        return base64.b64encode(encrypted_text).decode('utf-8')
    
    def encrypt_ecb_pad(self,text:str,is_base64:bool=True):
        """AES/CBC/PKCS5padding加密

        Args:
            text (str): 待加密字符串
            is_base64 (bool, optional): _description_. Defaults to True.

        Returns:
            _type_: _description_
        """
        mode = AES.MODE_ECB
        cipher = AES.new(self.key, mode)
        padded_data=pad(text.encode('utf-8'),AES.block_size)
        encrypted_text=cipher.encrypt(padded_data)
        if is_base64:
            return base64.b64encode(encrypted_text).decode('utf-8')
        else:
            return encrypted_text
        
    def decrypt_ecb_pad(self,encrypted_text:Union[str,bytes],is_base64:bool=True):
        """AES/CBC/PKCS5padding解密

        Args:
            encrypted_text (Union[str,bytes]): 待解密字符串/字节
            is_base64 (bool, optional): _description_. Defaults to True.

        Returns:
            _type_: _description_
        """
        mode = AES.MODE_ECB
        cipher = AES.new(self.key, mode)
        if is_base64:
            text = cipher.decrypt(base64.b64decode(encrypted_text))
        else:
            text = cipher.decrypt(encrypted_text)
        return unpad(text,AES.block_size).decode('utf-8')

    def decrypt_ecb(self, encrypted_text: str):
        """
        AES的CBC模式解密
        @param encrypted_text: 待解密字符串,base64
        @return:
        """
        mode = AES.MODE_ECB
        cipher = AES.new(self.key, mode)
        text = cipher.decrypt(base64.b64decode(encrypted_text))
        return text.decode('utf-8')