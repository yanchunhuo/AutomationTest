#
# rsa_tool.py
# @author yanchunhuo
# @description 
# @created 2022-03-04T14:25:11.785Z+08:00
# @last-modified 2022-03-04T17:08:23.332Z+08:00
#
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import base64

class RSA_Tool:
    def __init__(self) -> None:
        pass
    
    def rsa_encrypt(self,public_key,text:str,hashAlgo=None):
        """_summary_

        Args:
            public_key (_type_): _description_
            text (str): _description_
            hashAlgo (_type_, optional): The hash function to use. This can be a module under `Crypto.Hash`. Defaults to None.

        Returns:
            _type_: _description_
        """
        text=bytes(text,'utf-8')
        # 读取公钥
        public_key=RSA.import_key(bytes(public_key,'utf-8'))
        # 实例化加密套件
        cipher=PKCS1_OAEP.new(public_key,hashAlgo)
        encrypted_text=cipher.encrypt(text)
        return base64.b64encode(encrypted_text).decode('utf-8')
    
    def rsa_decrypt(self,private_key,encrypted_text:str,hashAlgo=None):
        """_summary_

        Args:
            private_key (_type_): _description_
            encrypted_text (str): _description_
            hashAlgo (_type_, optional): The hash function to use. This can be a module under `Crypto.Hash`. Defaults to None.

        Returns:
            _type_: _description_
        """
        encrypted_text=base64.b64decode(encrypted_text)
        # 读取私钥
        private_key=RSA.import_key(bytes(private_key,'utf-8'))
        # 实例化加密套件
        cipher=PKCS1_OAEP.new(private_key,hashAlgo)
        text=cipher.decrypt(encrypted_text)
        return text.decode('utf-8')
    
    def generator_key(self,bits:int=2048):
        key=RSA.generate(bits)
        private_key=key.export_key()
        public_key=key.publickey().export_key()
        return private_key,public_key