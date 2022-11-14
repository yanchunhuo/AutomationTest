#
# memcached_client.py
# @author yanchunhuo
# @description 
# @created 2021-10-18T15:05:34.469Z+08:00
# @last-modified 2021-10-18T17:43:35.744Z+08:00
# github https://github.com/yanchunhuo
import bmemcached

class Memcached_Client:
    def __init__(self,host:str,port:int=11211,username=None,password=None,timeout=3) -> None:
        self.client=bmemcached.Client(('%s:%s'%(host,port),),username=username,password=password,socket_timeout=timeout)
    
    def add(self,key:str, value:object, time=0, compress_level=-1):
        """不存在则添加,存在则不更新

        Args:
            key ([type]): [description]
            value ([type]): [description]
            time (int, optional): [description]. Defaults to 0.
            compress_level (int, optional): [description]. Defaults to -1.

        Returns:
            [type]: [description]
        """
        return self.client.add(key=key,value=value,time=time,compress_level=compress_level)\
    
    def set(self,key:str, value:object, time=0, compress_level=-1):
        return self.client.set(key=key,value=value,time=time,compress_level=compress_level)
    
    def set_multi(self,keys_vales:dict,time=0, compress_level=-1):
        return self.client.set_multi(mappings=keys_vales,time=time,compress_level=compress_level)
    
    def check_and_set(self,key:str, value:object, cas_key, time=0, compress_level=-1):
        """
        Args:
            key ([type]): [description]
            value ([type]): [description]
            cas_key ([type]): 通过self.get_value_and_cas_key()获取
            time (int, optional): [description]. Defaults to 0.
            compress_level (int, optional): [description]. Defaults to -1.

        Returns:
            [type]: [description]
        """
        return self.client.cas(key=key,value=value,cas=cas_key,time=time,compress_level=compress_level)
    
    def get(self,key:str,get_cas=False):
        return self.client.get(key=key,get_cas=get_cas)
    
    def get_multi(self,keys:list):
        return self.client.get_multi(keys=keys)
    
    def get_value_and_cas_key(self,key):
        return self.client.gets(key=key)
    
    def decr(self,key:str,value:int):
        """对存在的key进行递减，不存在返回0，存在返回递减后的值。最多只能递减到0

        Args:
            key (str): [description]
            value (int): [description]

        Returns:
            [type]: [description]
        """
        return self.client.decr(key=key,value=value)
    
    def incr(self,key:str,value:int):
        """对存在的key进行递增，不存在返回0，存在返回递增后的值

        Args:
            key (str): [description]
            value (int): [description]
        """
        return self.client.incr(key=key,value=value)
    
    def delete(self,key:str):
        return self.client.delete(key=key)

    def delete_multi(self,keys:list):
        return self.client.delete_multi(keys=keys)
        
    def replace(self,key:str,value:object,time=0,compress_level=-1):
        return self.client.replace(key=key,value=value,time=time,compress_level=compress_level)
    
    def flush_all(self,time=0):
        """
        Args:
            time (int, optional): 等待刷新的时间. Defaults to 0.
        """
        return self.client.flush_all(time=time)
    
    def get_server_stats(self,key:str=None):
        return self.client.stats(key=key)