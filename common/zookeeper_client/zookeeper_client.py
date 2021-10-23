#
# zookeeper_client.py
# @author yanchunhuo
# @description 
# @created 2021-10-20T19:00:30.289Z+08:00
# @last-modified 2021-10-23T15:21:52.316Z+08:00
# github https://github.com/yanchunhuo
from kazoo.client import KazooClient
from kazoo.client import KazooState
import os

class Zookeeper_Client:
    def __init__(self,hosts, timeout=10,read_only=None) -> None:
        self.hosts=hosts
        self.timeout=timeout
        self.read_only=read_only
        self._connect_server(hosts=self.hosts,timeout=self.timeout,read_only=self.read_only)
        
    def _connect_server(self,hosts, timeout=10,read_only=None):
        self.zk_client=KazooClient(hosts=hosts, timeout=timeout,read_only=read_only)
        self.zk_client.add_listener(self._listener)
        self.zk_client.start()
        
    def _listener(self,state):
        if state == KazooState.LOST:
            # 连接丢失重连
            self._connect_server(hosts=self.hosts,timeout=self.timeout,read_only=self.read_only)
        elif state == KazooState.SUSPENDED:
            # 连接断掉重连
            self._connect_server(hosts=self.hosts,timeout=self.timeout,read_only=self.read_only)
        else:
            # 正在连接、重连
            pass
    
    def create(self,path:str,value:bytes=b"",acl=None,makepath=False):
        if isinstance(value,str):
            value=bytes(value,'utf-8')
        return self.zk_client.create(path=path,value=value,acl=None,makepath=makepath)
            
    def ensure_path(self,path:str,acl=None):
        return self.zk_client.ensure_path(path=path,acl=None)
    
    def set(self,path:str,value:bytes=b"",version:int=-1):
        if isinstance(value,str):
            value=bytes(value,'utf-8')
        return self.zk_client.set(path=path,value=value,version=version)
        
    def exists(self,path:str):
        znodestat=self.zk_client.exists(path=path)
        return znodestat
    
    def get(self,path:str,is_return_stat:bool=False):
        data,znodestat=self.zk_client.get(path=path)
        if is_return_stat:
            return data,znodestat
        else:
            return data.decode('utf-8')
    
    def get_children_names(self,path:str)->list:
        return self.zk_client.get_children(path=path)
    
    def get_children_paths(self,path:str)->list:
        paths=[]
        names=self.zk_client.get_children(path=path)
        if not path.endswith('/'):
            path+='/'
        for name in names:
            paths.append(os.path.join(path,name))
        return paths
        
    def delete(self,path:str,version=-1,recursive:bool=False):
        return self.zk_client.delete(path=path,version=version,recursive=recursive)        