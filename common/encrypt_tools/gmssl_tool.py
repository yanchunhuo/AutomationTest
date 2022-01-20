#
# sm_tool.py
# @author yanchunhuo
# @description 
# @created 2021-09-06T17:01:21.635Z+08:00
# @last-modified 2022-01-20T11:54:15.278Z+08:00
# github https://github.com/yanchunhuo
from common.encrypt_tools.gmssl.sm2 import CryptSM2
from common.encrypt_tools.gmssl.sm4 import CryptSM4
from common.encrypt_tools.gmssl.sm4 import SM4_ENCRYPT
from common.encrypt_tools.gmssl.sm4 import SM4_DECRYPT
from common.encrypt_tools.gmssl import func

class GMSSL_Tool:
    def __init__(self,sm2_private_key:str=None,sm2_public_key:str=None,sm4_key:str=None,sm4_iv_cbc:str=None,is_sm4_key_use_hex=True) -> None:
        """[summary]

        Args:
            sm2_private_key (str, optional): [description]. Defaults to None.
            sm2_public_key (str, optional): [description]. Defaults to None.
            sm4_key (str, optional): [description]. Defaults to None.
        """
        self.sm2_private_key=sm2_private_key
        self.sm2_public_key=sm2_public_key
        self.sm2_crypt=CryptSM2(private_key=self.sm2_private_key,public_key=self.sm2_public_key)
        if not sm4_key is None:
            if is_sm4_key_use_hex:
                self.sm4_key=bytes.fromhex(sm4_key)
            else:
                self.sm4_key=bytes(sm4_key,'utf-8')
            self.sm4_encrypt=CryptSM4()
            self.sm4_decrypt=CryptSM4()
            self.sm4_encrypt.set_key(self.sm4_key,SM4_ENCRYPT)
            self.sm4_decrypt.set_key(self.sm4_key,SM4_DECRYPT)
        if not sm4_iv_cbc is None:
            self.sm4_iv_cbc=bytes(sm4_iv_cbc,'utf-8')
        
    def sm2_encrypt(self,text:str)->bytes:
        if not isinstance(text,bytes):
            text=bytes(text,encoding='utf-8')
        return self.sm2_crypt.encrypt(text)
    
    def sm2_decrypt(self,encrypt_data:bytes)->str:
        return self.sm2_crypt.decrypt(encrypt_data).decode('utf-8')
    
    def sm2_sign(self,text:str)->str:
        if not isinstance(text,bytes):
            text=bytes(text,encoding='utf-8')
        random_hex_str=func.random_hex(self.sm2_crypt.para_len)
        sign=self.sm2_crypt.sign(text,random_hex_str) #  16进制
        return sign
    
    def sm2_verify(self,text:str,sign:str)->bool:
        if not isinstance(text,bytes):
            text=bytes(text,encoding='utf-8')
        result=self.sm2_crypt.verify(sign,text)#  16进制
        return result
    
    def sm3_sign(self,text:str)->str:
        if not isinstance(text,bytes):
            text=bytes(text,encoding='utf-8')
        random_hex_str=func.random_hex(self.sm2_crypt.para_len)
        sign=self.sm2_crypt.sign_with_sm3(text,random_hex_str) #  16进制
        return sign
    
    def sm3_verify(self,text:str,sign:str)->bool:
        if not isinstance(text,bytes):
            text=bytes(text,encoding='utf-8')
        result=self.sm2_crypt.verify_with_sm3(sign,text)#  16进制
        return result
    
    def sm4_encrypt_ecb(self,text:str)->bytes:
        if not isinstance(text,bytes):
            text=bytes(text,encoding='utf-8')
        return self.sm4_encrypt.crypt_ecb(text)
    
    def sm4_decrypt_ecb(self,encrypt_data:bytes)->str:
        return self.sm4_decrypt.crypt_ecb(encrypt_data).decode('utf-8')

    def sm4_encrypt_cbc(self,text:str)->bytes:
        if not isinstance(text,bytes):
            text=bytes(text,encoding='utf-8')
        return self.sm4_encrypt.crypt_cbc(self.sm4_iv_cbc,text)
    
    def sm4_decrypt_cbc(self,encrypt_data:bytes)->str:
        return self.sm4_decrypt.crypt_cbc(self.sm4_iv_cbc,encrypt_data).decode('utf-8')