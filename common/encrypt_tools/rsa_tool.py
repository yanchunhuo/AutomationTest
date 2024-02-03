#
# rsa_tool.py
# @author yanchunhuo
# @description 
# @created 2022-03-04T14:25:11.785Z+08:00
# @last-modified 2024-02-03T11:39:00.393Z+08:00
#
from Crypto.Cipher import PKCS1_OAEP,PKCS1_v1_5
from Crypto.PublicKey import RSA
import base64

class RSATool:
    def __init__(self) -> None:
        pass
    
    def rsa_encrypt(self,public_key,text:str,hashAlgo=None,cipher_type:str='pkcs1_oaep'):
        """_summary_

        Args:
            public_key (_type_): 字符串前需加"-----BEGIN PUBLIC KEY-----\n",字符串后需加"\n-----END PUBLIC KEY-----"
            text (str): _description_
            hashAlgo (_type_, optional): _description_. Defaults to None.
            cipher_type (str, optional): pkcs1_oaep、pkcs1_v1_5. Defaults to 'pkcs1_oaep'.

        Returns:
            _type_: _description_
        """
        text=bytes(text,'utf-8')
        # 读取公钥
        public_key=RSA.import_key(bytes(public_key,'utf-8'))
        # 实例化加密套件
        if cipher_type.lower()=='pkcs1_oaep':
            cipher=PKCS1_OAEP.new(public_key,hashAlgo)
        elif cipher_type.lower()=='pkcs1_v1_5':
            cipher=PKCS1_v1_5.new(public_key)
        encrypted_text=cipher.encrypt(text)
        return base64.b64encode(encrypted_text).decode('utf-8')
    
    def rsa_decrypt(self,private_key,encrypted_text:str,hashAlgo=None,cipher_type:str='pkcs1_oaep'):
        """_summary_

        Args:
            private_key (_type_): 字符串前需加"-----BEGIN RSA PRIVATE KEY-----\n",字符串后需加"\n-----END RSA PRIVATE KEY-----"
            encrypted_text (str): _description_
            hashAlgo (_type_, optional): _description_. Defaults to None.
            cipher_type (str, optional): pkcs1_oaep、pkcs1_v1_5. Defaults to 'pkcs1_oaep'.

        Returns:
            _type_: _description_
        """
        encrypted_text=base64.b64decode(encrypted_text)
        # 读取私钥
        private_key=RSA.import_key(bytes(private_key,'utf-8'))
        # 实例化加密套件
        if cipher_type.lower()=='pkcs1_oaep':
            cipher=PKCS1_OAEP.new(private_key,hashAlgo)
        elif cipher_type.lower()=='pkcs1_v1_5':
            cipher=PKCS1_v1_5.new(private_key)
        text=cipher.decrypt(encrypted_text)
        return text.decode('utf-8')
    
    def generator_key(self,bits:int=2048):
        key=RSA.generate(bits)
        private_key=key.export_key()
        public_key=key.publickey().export_key()
        return private_key,public_key